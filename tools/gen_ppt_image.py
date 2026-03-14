#!/usr/bin/env python3
"""
PPT 页面图片生成工具（纯 Python，零外部依赖）

被每页的 gen.py 调用，提供并发图片生成能力。
直接调用 Gemini generateContent API，支持参考图上传。

使用方法:
    from gen_ppt_image import gen
    gen(prompt="...", page_dir="ppt-pages/01/init", count=3)

配置:
    项目根目录 .env 文件:
        API_URL=https://your-api-endpoint
        API_KEY=your-api-key
        MODEL=gemini-2.0-flash-preview-image-generation
        IMAGE_SIZE=4K
"""

import base64
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parent.parent


# ── .env 解析 ──────────────────────────────────────────────

def _load_env(env_path: Path) -> dict:
    """解析 .env 文件，返回键值对字典"""
    env = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        # 去除引号
        value = value.strip().strip("'\"")
        env[key.strip()] = value
    return env


def _get_config() -> dict:
    """从 .env 读取配置"""
    env = _load_env(ROOT / ".env")
    api_url = env.get("API_URL", "")
    api_key = env.get("API_KEY", "")
    model = env.get("MODEL", "gemini-2.0-flash-preview-image-generation")
    image_size = env.get("IMAGE_SIZE", "4K")

    if not api_url or not api_key:
        print("[错误] 请在项目根目录创建 .env 文件，配置 API_URL 和 API_KEY")
        print("  格式：")
        print("    API_URL=https://your-api-endpoint")
        print("    API_KEY=your-api-key")
        print("    MODEL=gemini-2.0-flash-preview-image-generation")
        print("    IMAGE_SIZE=4K")
        sys.exit(1)

    return {
        "api_url": api_url.rstrip("/"),
        "api_key": api_key,
        "model": model,
        "image_size": image_size,
    }


# ── 参考图处理 ─────────────────────────────────────────────

_MIME_MAP = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def _read_image_base64(image_path: Path) -> tuple:
    """读取图片并返回 (base64_data, mime_type)"""
    data = image_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    mime = _MIME_MAP.get(image_path.suffix.lower(), "image/png")
    return b64, mime


# ── Gemini API 调用 ────────────────────────────────────────

def _build_url(config: dict) -> str:
    """构建 Gemini generateContent 端点 URL"""
    api_url = config["api_url"]
    model = config["model"]
    # 规范化 model 名称
    if model.startswith("models/"):
        model = model[len("models/"):]

    # 兼容不同 base URL 格式
    if "/v1beta" in api_url:
        return f"{api_url}/models/{model}:generateContent"
    else:
        return f"{api_url}/v1beta/models/{model}:generateContent"


def _build_body(prompt: str, ref_path: Path | None,
                image_size: str, aspect_ratio: str) -> dict:
    """构建请求体"""
    parts = []

    # 参考图放在前面
    if ref_path and ref_path.exists():
        b64, mime = _read_image_base64(ref_path)
        parts.append({"inlineData": {"data": b64, "mimeType": mime}})

    # Prompt 文本（附加宽高比信息）
    text = prompt
    if aspect_ratio:
        text = f"{prompt} Aspect ratio: {aspect_ratio}."
    parts.append({"text": text})

    # imageConfig
    image_config = {"imageSize": image_size}
    if aspect_ratio:
        image_config["aspectRatio"] = aspect_ratio

    return {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": image_config,
        },
    }


def _call_api(config: dict, body: dict) -> bytes | None:
    """调用 Gemini API，返回图片二进制数据"""
    url = _build_url(config)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api_key']}",
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"API 错误 ({e.code}): {err_body}") from e

    # 从响应中提取图片数据
    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData", {})
            b64_data = inline.get("data", "")
            if b64_data:
                return base64.b64decode(b64_data)

    return None


# ── 单张生成（供进程池调用）──────────────────────────────────

def _generate_one(prompt: str, output_path: str, ref: str | None,
                   image_size: str, aspect_ratio: str) -> tuple:
    """
    生成单张图片，自动重试一次。
    返回 (success: bool, message: str)
    """
    config = _get_config()
    ref_path = Path(ref) if ref else None
    if ref_path and not ref_path.is_absolute():
        ref_path = ROOT / ref_path

    body = _build_body(prompt, ref_path, image_size, aspect_ratio)
    out = Path(output_path)

    for attempt in range(2):
        try:
            img_data = _call_api(config, body)
            if img_data:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(img_data)
                return True, str(out)
            else:
                if attempt == 0:
                    time.sleep(2)
                    continue
                return False, f"API 返回无图片数据: {out}"
        except Exception as e:
            if attempt == 0:
                time.sleep(2)
                continue
            return False, f"生成失败: {e}"

    return False, f"未知错误: {out}"


# ── 公共接口 ───────────────────────────────────────────────

def gen(
    prompt: str,
    page_dir: str,
    count: int = 3,
    ref: str = None,
    aspect_ratio: str = "16:9",
    image_size: str = None,
    prefix: str = "v",
):
    """
    并发生成多张候选图

    Args:
        prompt:       图片描述（Prompt）
        page_dir:     输出目录（绝对或相对路径）
        count:        候选图数量，默认 3
        ref:          参考图路径（可选，用于风格锚定）
        aspect_ratio: 宽高比，默认 16:9
        image_size:   分辨率 1K / 2K / 4K（默认从 .env 读取）
        prefix:       文件名前缀，默认 "v"（生成 v1.png, v2.png, v3.png）
    """
    # 如果未指定 image_size，从 .env 读取
    if image_size is None:
        config = _get_config()
        image_size = config["image_size"]

    page_path = Path(page_dir)
    page_path.mkdir(parents=True, exist_ok=True)

    tasks = []
    for i in range(1, count + 1):
        output_path = str(page_path / f"{prefix}{i}.png")
        tasks.append((prompt, output_path, ref, image_size, aspect_ratio))

    print(f"[生成中] {count} 张候选图...")
    print(f"[Prompt] {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    if ref:
        print(f"[参考图] {ref}")

    results = []
    with ProcessPoolExecutor(max_workers=count) as pool:
        futures = {
            pool.submit(_generate_one, *task): task[1]
            for task in tasks
        }
        for future in as_completed(futures):
            ok, msg = future.result()
            tag = "✓" if ok else "✗"
            print(f"  [{tag}] {msg}")
            results.append((ok, msg))

    success = sum(1 for ok, _ in results if ok)
    print(f"\n[完成] {success}/{count} 张生成成功")

    if success == 0:
        print("[提示] 全部失败，请检查 .env 中的 API_URL 和 API_KEY 是否正确")
