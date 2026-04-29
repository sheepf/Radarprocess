# Radarprocess

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

基于有向无环图 (DAG) 的雷达信号处理框架。本项目旨在提供一个高度可扩展、模块化的雷达信号处理流水线构建工具，通过 DAG 架构优化计算资源的调度、节点解耦与并行处理，加速雷达算法从原型到工程的落地。

## 🌟 主要特性 (Features)

- **DAG 任务调度**: 基于 `radar_dag` 核心模块，支持将复杂的雷达信号处理算法（如脉冲压缩、MTI、CFAR等）拆解为独立的计算图节点。
- **模块化设计**: 算子间相互解耦，易于开发、测试和插入新的自定义信号处理算子。
- **现代化构建**: 采用现代 Python 项目构建标准 (`pyproject.toml`)，环境依赖管理更清晰。
- **AI 协同开发**: 包含 `.claude` 规范，对 AI 辅助生成代码与重构具有良好的兼容性。

## 📂 目录结构 (Repository Structure)

```text
Radarprocess/
├── src/
│   └── radar_dag/       # 核心业务代码：实现基于 DAG 的雷达算法流水线与计算图
├── examples/            # 示例代码：展示如何快速构建和运行不同的雷达处理任务图
├── tests/               # 单元测试：确保各算子逻辑和 DAG 调度的正确性与鲁棒性
├── .claude/             # AI 助手环境配置与上下文记忆
├── CLAUDE.md            # 项目 AI 交互规范及开发说明
├── pyproject.toml       # Python 项目配置及依赖管理文件
└── .gitignore           # Git 忽略文件配置
