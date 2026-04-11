# 🚀 中国区 GitHub 和 Docker 加速镜像

本仓库自动收集和更新适用于中国区的 GitHub 文件加速和 Docker 镜像加速地址。

## 📊 统计信息

- **最后更新**: 2026-04-11 03:36:59
- **GitHub 镜像数量**: 11
- **Docker 镜像数量**: 10

## 🔥 GitHub 文件加速

以下是经过验证的 GitHub 文件加速镜像地址：

- https://cors.isteed.cc
- https://dockerproxy.link
- https://dockerproxy.net
- https://gh-proxy.com
- https://gh.ddlc.top
- https://gh.xmly.dev
- https://ghfast.top
- https://ghproxy.1888866.xyz
- https://github.abskoop.workers.dev
- https://proxy.vvvv.ee
- https://user:TOKEN@ghproxy.com

### 📖 使用方法

将原始的 GitHub 文件链接前缀替换为镜像地址：

```bash
# 原始链接
https://github.com/user/repo/releases/download/v1.0/file.zip

# 加速链接
https://镜像地址/https://github.com/user/repo/releases/download/v1.0/file.zip
```

## 🐳 Docker 镜像加速

以下是收集到的 Docker 镜像加速地址：

- ccr.ccs.tencentyun.com
- docker.m.daocloud.io
- dockerhub.icu
- hub.rat.dev
- registry.cn-beijing.aliyuncs.com
- registry.cn-hangzhou.aliyuncs.com
- registry.cn-qingdao.aliyuncs.com
- registry.cn-shanghai.aliyuncs.com
- registry.cn-shenzhen.aliyuncs.com
- registry.cn-zhangjiakou.aliyuncs.com

### 📖 使用方法

配置 Docker 镜像加速器：

```bash
# 创建或编辑 /etc/docker/daemon.json
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://registry.cn-hangzhou.aliyuncs.com"
  ]
}
EOF

# 重启 Docker 服务
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 📝 数据来源

镜像地址来源于以下项目：

- [hunshcn/gh-proxy](https://github.com/hunshcn/gh-proxy)
- [XIU2/TrackersListCollection](https://github.com/XIU2/TrackersListCollection)
- [521xueweihan/GitHub520](https://github.com/521xueweihan/GitHub520)
- [dongyubin/DockerHub](https://github.com/dongyubin/DockerHub)

## 🔄 自动更新

本仓库通过 GitHub Actions 每天自动更新镜像地址列表。

## ⚠️ 免责声明

- 本项目仅收集公开可用的镜像地址
- 请根据实际情况选择合适的镜像地址
- 使用镜像服务时请遵守相关服务条款

---

**最后更新时间**: 2026-04-11 03:36:59
