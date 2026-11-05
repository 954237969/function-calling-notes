# Function Calling 笔记

使用 VitePress 构建的个人学习笔记网站。

## 本地使用

```bash
pnpm install --frozen-lockfile
pnpm docs:dev
pnpm docs:build
pnpm docs:preview
```

Node 24 / pnpm 9.15.0 / VitePress 1.6.3。

## 内容

- notes/function-calling.md：正文、Scaling Law 公式与关联知识
- notes/assets/：10 张原笔记配图，以无损 WebP 保存
- code/：原文中的代码片段（未执行模型 API 验证）
- .github/workflows/deploy.yml：GitHub Pages 自动构建部署

## 整理范围

来源为个人 Notion 笔记“Function calling”。未导出数据库属性、关联项目、页面权限、用户标识或文末内嵌数据库。原 Notion 页面未修改。正文仅作展示格式转换，未声称完成技术审校。

图片与教学内容保留原资料的权利范围；未对第三方素材授予额外许可。

## 部署

仓库 Pages Source 选择 GitHub Actions 后，推送 main 分支触发构建。部署状态以 Actions 和 Pages 实际返回地址为准。
