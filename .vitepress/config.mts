import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Function Calling 笔记',
  description: '函数调用、工具定义、Agent 与 Scaling Law 学习笔记',
  lang: 'zh-CN',
  base: '/function-calling-notes/',
  cleanUrls: true,
  srcExclude: ['code/**', 'README.md', 'PUBLISH.md'],
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '阅读笔记', link: '/notes/function-calling' },
      { text: '配套代码', link: 'https://github.com/954237969/function-calling-notes/tree/main/code' }
    ],
    sidebar: [{ text: 'Function Calling', items: [
      { text: '完整笔记', link: '/notes/function-calling' },
      { text: '缩放定律拓展', link: '/notes/function-calling#拓展-缩放定律-scaling-law' },
      { text: '概念与工作原理', link: '/notes/function-calling#一、什么是function-call' },
      { text: '工具定义与使用', link: '/notes/function-calling#三、function-call-使用方式' },
      { text: 'Agent 调用工具', link: '/notes/function-calling#四、agent-调用-tool' }
    ] }],
    outline: { label: '本页目录', level: [2, 3] },
    search: { provider: 'local' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '目录',
    darkModeSwitchLabel: '主题',
    socialLinks: [{ icon: 'github', link: 'https://github.com/954237969/function-calling-notes' }]
  },
  markdown: { math: true, lineNumbers: true, image: { lazyLoading: true } }
})
