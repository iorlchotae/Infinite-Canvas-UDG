# 无限画布 · Infinite Canvas（UDG 版）

**联创四院（UDG）** 基于开源项目 [Infinite-Canvas](https://github.com/hero8152/Infinite-Canvas) 二次开发的画布软件。

- 项目主页：<https://github.com/iorlchotae/Infinite-Canvas-UDG>

---

## 项目简介

无限画布（UDG 版）是一款本地运行的 AI 创作画布工具，以 Python + FastAPI 为后端、原生前端为界面，支持调用各类 OpenAI 协议 API、ModelScope 免费模型等，把生成、编辑、整理、沉淀整合到一张无限画布上。

相比原版，UDG 版聚焦画布核心体验：

- **去掉本地功能板块**：移除原「本地功能」（文生图 / 细节增强 / 图片编辑 / 角度控制）入口，画布能力不受影响
- **去掉 GPT 对话板块**：移除独立 GPT 对话页面，AI 能力统一收敛到画布节点
- **全新品牌**：界面署名更新为「联创四院 / UDG」
- **独立仓库**：项目主页与在线更新均指向 UDG 独立仓库

## 功能特性

1. 无限画布：节点式创作流，支持文生图 / 图生图 / 局部重绘 / 扩展出图 / 九宫格多视角等
2. 在线生图：直连云端 API 生成
3. 素材库：本地素材分组管理，支持 Chrome 批量采集插件、Photoshop 直连插件（tools 目录）
4. API 设置：管理各平台地址、模型列表与 Key（Key 写入后端 env，页面不回显）
5. 一键更新：从 GitHub 仓库自动下载新版本（更新前自动备份，可回滚）
6. 支持几乎所有 OpenAI 协议的 API / 异步协议 / Gemini 协议 / 方钩协议
7. 支持 ModelScope 免费 LLM 与图像模型调用
8. 支持即梦 CLI、GPT CLI、Antigravity CLI 调用

## 快速开始

### 部署到一台新电脑（Windows）

整个文件夹（含 `python/` 便携运行时与 `packages/` 离线依赖包）**整体拷贝**到新电脑任意目录，双击 `start.bat` 即可使用：

- **无需安装 Python**：优先使用项目自带的 `python/` 便携运行时
- **无需联网**：依赖已随项目打包；即使依赖丢失，`start.bat` 会自动调用 `install-deps.bat` 从 `packages/` 离线修复
- **端口自动避让**：3000 被占用时自动顺延到 3001、3002……，控制台会显示实际访问地址，浏览器自动打开对应页面
- **双击 `run.bat` 效果相同**（兼容入口，内部转发到 `start.bat`）

```bat
start.bat
```

启动后按控制台提示访问（默认 <http://127.0.0.1:3000/>，被占用时顺延）。

### macOS / Linux

```bash
python3 main.py
```

或使用 `mac-启动服务.sh`。

> macOS 首次运行如遇权限提示，请先执行 `mac-修复权限.command`。

首次使用请进入「API 设置」配置可用的 API 平台与 Key；画布仅保留 OpenAI 协议、ModelScope、火山引擎、即梦等图像/对话能力，原 ComfyUI / RunningHub / MiniMax / LTX Director / 视频生成节点已移除。

## 配套工具

- `tools/chrome-local-asset-importer`：Chrome 插件，扫描网页图片批量导入素材库
- `tools/photoshop-asset-connector`：Photoshop UXP 面板插件，PS 与素材库双向打通

## 开源与致谢

本项目基于 **wuli大雄** 的开源项目 [Infinite-Canvas](https://github.com/hero8152/Infinite-Canvas) 二次开发而成。

**特别致谢**：感谢原创作者 **wuli大雄** 开发并开源了 Infinite-Canvas，为本项目提供了全部基础代码。原项目已申请著作权，其开源约定（二次开发须保持开源并注明来源作者、禁止擅自商用封装）对上游代码继续适用，本项目同样保持开源并注明来源。

UDG 版的改动包括：移除本地功能与 GPT 对话板块、界面署名替换为联创四院（UDG）、更新源切换至本仓库等。

## 目录结构

```
main.py                 # FastAPI 后端入口
static/                 # 前端页面（画布 / 素材库 / 设置等）
static/js/              # 前端脚本
static/images/          # 图片资源
data/                   # 运行数据（画布、素材库、配置）
tools/                  # Chrome 采集插件 / Photoshop 直连插件 / 端口探测脚本
packages/               # 离线依赖包（与自带 Python 版本匹配的 wheel）
python/                 # Windows 便携 Python 运行时（含已装依赖）
start.bat               # Windows 启动入口（依赖自检 + 端口避让）
install-deps.bat        # 依赖安装脚本（优先离线，支持无网环境）
run.bat                 # 兼容启动入口（转发到 start.bat）
```

## 常见问题

- **端口被占用**：无需手动处理——启动时自动检测，3000 被占用会顺延到 3001/3002……，以控制台输出的地址为准。如需固定端口，可设置环境变量 `CANVAS_PORT`（如 `set CANVAS_PORT=8080` 后再运行 `start.bat`）。
- **提示缺少依赖 / ModuleNotFoundError**：`start.bat` 会自动从 `packages/` 离线补装；也可手动运行 `install-deps.bat`。请勿删除 `packages/` 与 `python/` 目录。
- **更新失败**：请先在本页「一键更新 → 测试连通性」检查 GitHub 各节点；国内网络请配置系统代理。
- **想关闭更新提示**：删除根目录的 `VERSION` 文件即可。
