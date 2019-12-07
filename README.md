[TOC]

# what is note-press?

一个用来解析主流笔记的项目。

- 你需要的是一个发布的平台，而不是一个写作的平台。写作平台可以用专业的服务商代替，但是它们没做的是如何让你的内容分享出去。当然你可以自己搭建博客网站，但是这样维护太过麻烦，你同样也需要一个专业的提供商，因为它可以省去你维护的烦恼，Github Pages 可能是一个更好的选择。
- 这时候问题就来了，写作是在笔记平台，分享却在另一个平台。如何在修改之后及时更新呢？note-press 就帮你做了这么一个功能。

# what you should know?

`notes.yml` 格式如下：

```yaml
- url: https://note.youdao.com/ynoteshare1/index.html?id=fcea783dfde1b52ae026773b1b5fba05&type=note
  utime: # to judge the article if need to refresh
  aid:  # which represent the Article's ID，冗余
  title: # 标题，冗余字段
  ctime: # 创建时间，冗余字段
  publish: false # 预留，用于下架
```

# 有道云笔记

- 仅支持 markdown 格式

## 通过命令行形式

- 发布文章

在 notes.yml 添加链接

- 更新文章

运行一遍命令：xxx ，即可



- 下架文章

todo,可以定义一个属性


# node-press 的设计流程：

https://www.processon.com/view/link/5deb4928e4b079080a235c68