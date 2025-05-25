#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主爬虫脚本 - 集成所有功能的统一入口
包含：数据爬取、验证、清理、修复、文档生成
"""

import requests
import re
import json
import time
import logging
from datetime import datetime
from typing import Set, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MirrorCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 20
        self.github_mirrors = set()
        self.docker_mirrors = set()

        # 数据源配置
        self.github_repos = [
            "hunshcn/gh-proxy",
            "XIU2/TrackersListCollection",
            "521xueweihan/GitHub520",
            "fhefh2015/Fast-GitHub",
            "RC1844/FastGithub",
            "dotnetcore/FastGithub",
            "dongyubin/DockerHub"
        ]

        # 预设的已知镜像
        self.known_github_mirrors = {
            "https://gh-proxy.com",
            "https://ghfast.top",
            "https://hub.gitmirror.com",
            "https://github.moeyy.xyz",
            "https://gh.ddlc.top",
            "https://gh.xmly.dev",
            "https://ghps.cc",
            "https://git.886.be",
            "https://github.abskoop.workers.dev",
            "https://ghproxy.net",
            "https://gh.con.sh",
            "https://cors.isteed.cc",
            "https://ghproxy.fsou.cc",
            "https://ghproxy.1888866.xyz",
            "https://fastgit.org",
        }

        self.known_docker_mirrors = {
            "docker.m.daocloud.io",
            "registry.cn-hangzhou.aliyuncs.com",
            "registry.cn-shanghai.aliyuncs.com",
            "registry.cn-beijing.aliyuncs.com",
            "registry.cn-shenzhen.aliyuncs.com",
            "ccr.ccs.tencentyun.com",
            "hub-mirror.c.163.com",
            "mirror.baidubce.com",
            "registry.docker-cn.com",
            "docker.mirrors.ustc.edu.cn",
            "reg-mirror.qiniu.com",
            "registry.cn-qingdao.aliyuncs.com",
            "registry.cn-zhangjiakou.aliyuncs.com"
        }

    def fetch_content(self, url: str) -> str:
        """获取网页内容"""
        try:
            logger.info(f"正在获取: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"获取 {url} 失败: {e}")
            return ""

    def extract_github_mirrors(self, content: str) -> Set[str]:
        """从内容中提取 GitHub 镜像地址"""
        mirrors = set()

        # GitHub 镜像模式
        patterns = [
            r'https://[^/\s]*(?:gh|github|proxy|mirror|fast)[^/\s]*\.[^/\s]+',
            r'https://[^/\s]+\.(?:workers\.dev|cf|vercel\.app|herokuapp\.com|netlify\.app)',
            r'https://(?:gh-proxy|ghfast|ghproxy|ghps)\.[^/\s]+',
            r'https://hub\.gitmirror\.com',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                clean_url = match.strip().rstrip('/')
                if self.is_valid_github_mirror(clean_url):
                    mirrors.add(clean_url)

        return mirrors

    def extract_docker_mirrors(self, content: str) -> Set[str]:
        """从内容中提取 Docker 镜像地址"""
        mirrors = set()

        patterns = [
            r'[^/\s]*\.(?:aliyuncs\.com|tencentcloudcr\.com)',
            r'docker\.m\.daocloud\.io',
            r'ccr\.ccs\.tencentyun\.com',
            r'hub-mirror\.c\.163\.com',
            r'mirror\.baidubce\.com',
            r'registry\.docker-cn\.com',
            r'docker\.mirrors\.ustc\.edu\.cn',
            r'reg-mirror\.qiniu\.com',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                clean_url = match.strip().rstrip('/')
                if self.is_valid_docker_mirror(clean_url):
                    mirrors.add(clean_url)

        return mirrors

    def is_valid_github_mirror(self, url: str) -> bool:
        """验证是否为有效的 GitHub 镜像"""
        if not url.startswith('https://'):
            return False

        # 排除明显不是镜像的域名
        exclude_patterns = [
            r'github\.com', r'raw\.githubusercontent\.com', r'api\.github\.com',
            r'img\.shields\.io', r'cdn\.jsdelivr\.net', r'docs\.docker\.com',
            r'blog\.', r'cdn\.', r'web\.archive\.org', r'\.png$', r'\.jpg$', r'\.svg'
        ]

        for pattern in exclude_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False

        return len(url) > 10

    def is_valid_docker_mirror(self, url: str) -> bool:
        """验证是否为有效的 Docker 镜像"""
        if not url or '.' not in url:
            return False

        # 排除无效的模式
        if '<' in url or '>' in url or 'your_code' in url:
            return False

        valid_patterns = [
            r'\.aliyuncs\.com$', r'\.tencentcloudcr\.com$', r'docker\.m\.daocloud\.io$',
            r'ccr\.ccs\.tencentyun\.com$', r'hub-mirror\.c\.163\.com$',
            r'mirror\.baidubce\.com$', r'registry\.docker-cn\.com$',
            r'docker\.mirrors\.ustc\.edu\.cn$', r'reg-mirror\.qiniu\.com$'
        ]

        return any(re.search(pattern, url) for pattern in valid_patterns)

    def crawl_github_repos(self):
        """爬取 GitHub 仓库"""
        logger.info("🔍 开始爬取 GitHub 仓库...")

        for repo in self.github_repos:
            try:
                # 尝试 master 分支
                readme_url = f"https://raw.githubusercontent.com/{repo}/master/README.md"
                content = self.fetch_content(readme_url)

                if not content:
                    # 尝试 main 分支
                    readme_url = f"https://raw.githubusercontent.com/{repo}/main/README.md"
                    content = self.fetch_content(readme_url)

                if content:
                    github_mirrors = self.extract_github_mirrors(content)
                    self.github_mirrors.update(github_mirrors)

                    docker_mirrors = self.extract_docker_mirrors(content)
                    self.docker_mirrors.update(docker_mirrors)

                time.sleep(1)  # 避免请求过于频繁

            except Exception as e:
                logger.error(f"爬取仓库 {repo} 失败: {e}")

    def add_known_mirrors(self):
        """添加已知的镜像地址"""
        logger.info("📋 添加已知镜像地址...")
        self.github_mirrors.update(self.known_github_mirrors)
        self.docker_mirrors.update(self.known_docker_mirrors)

    def test_github_mirror_content(self, mirror_url: str) -> dict:
        """测试 GitHub 镜像的内容下载功能"""
        test_file_url = "https://gist.githubusercontent.com/weekoo2025/7a8bcb034d5d223384101b8c4773089a/raw/all.txt"
        test_url = f"{mirror_url}/{test_file_url}"

        result = {
            'url': mirror_url,
            'status': 'unknown',
            'response_time': None,
            'content_valid': False
        }

        try:
            start_time = time.time()
            response = self.session.get(test_url, timeout=self.timeout)
            response_time = time.time() - start_time

            result['response_time'] = round(response_time * 1000, 2)

            if response.status_code == 200:
                content = response.text.strip()

                # 验证内容有效性
                if (len(content) > 50 and
                    ('http' in content.lower() or 'docker' in content.lower() or
                     'registry' in content.lower() or 'mirror' in content.lower())):
                    result['status'] = 'available'
                    result['content_valid'] = True
                else:
                    result['status'] = 'content_invalid'
            else:
                result['status'] = 'http_error'

        except Exception as e:
            result['status'] = 'error'

        return result

    def validate_github_mirrors(self):
        """验证 GitHub 镜像的可用性"""
        logger.info("🧪 开始验证 GitHub 镜像...")

        valid_mirrors = []

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_url = {executor.submit(self.test_github_mirror_content, url): url
                           for url in self.github_mirrors}

            for future in as_completed(future_to_url):
                result = future.result()

                if result['content_valid']:
                    valid_mirrors.append(result['url'])
                    logger.info(f"✅ {result['url']} ({result['response_time']}ms)")
                else:
                    logger.warning(f"❌ {result['url']} - {result['status']}")

        self.github_mirrors = set(valid_mirrors)
        logger.info(f"📊 GitHub 镜像验证完成: {len(valid_mirrors)} 个可用")

    def generate_mirrors_json(self):
        """生成 mirrors.json 文件"""
        logger.info("📄 生成 mirrors.json...")

        # 清理 Docker 镜像格式
        clean_docker_mirrors = []
        for url in self.docker_mirrors:
            clean_url = url.replace('https://', '').replace('http://', '')
            clean_docker_mirrors.append(clean_url)

        data = {
            'update_time': datetime.now().isoformat(),
            'github_mirrors': {
                'count': len(self.github_mirrors),
                'urls': sorted(list(self.github_mirrors))
            },
            'docker_mirrors': {
                'count': len(clean_docker_mirrors),
                'urls': sorted(list(set(clean_docker_mirrors)))
            }
        }

        with open('mirrors.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ mirrors.json 生成完成")
        logger.info(f"📊 GitHub 镜像: {len(self.github_mirrors)} 个")
        logger.info(f"📊 Docker 镜像: {len(clean_docker_mirrors)} 个")

    def generate_readme(self):
        """生成 README.md 文件"""
        logger.info("📝 生成 README.md...")

        try:
            with open('mirrors.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            logger.error("无法读取 mirrors.json")
            return

        github_mirrors = data['github_mirrors']['urls']
        docker_mirrors = data['docker_mirrors']['urls']
        update_time = data['update_time']

        # 格式化更新时间
        try:
            dt = datetime.fromisoformat(update_time.replace('Z', '+00:00'))
            formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_time = update_time

        readme_content = f"""# 🚀 中国区 GitHub 和 Docker 加速镜像

本仓库自动收集和更新适用于中国区的 GitHub 文件加速和 Docker 镜像加速地址。

## 📊 统计信息

- **最后更新**: {formatted_time}
- **GitHub 镜像数量**: {len(github_mirrors)}
- **Docker 镜像数量**: {len(docker_mirrors)}

## 🔥 GitHub 文件加速

以下是经过验证的 GitHub 文件加速镜像地址：

"""

        for mirror in github_mirrors:
            readme_content += f"- {mirror}\n"

        readme_content += f"""
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

"""

        for mirror in docker_mirrors:
            readme_content += f"- {mirror}\n"

        readme_content += f"""
### 📖 使用方法

配置 Docker 镜像加速器：

```bash
# 创建或编辑 /etc/docker/daemon.json
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://registry.cn-hangzhou.aliyuncs.com"
  ]
}}
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

**最后更新时间**: {formatted_time}
"""

        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)

        logger.info("✅ README.md 生成完成")

    def run(self):
        """运行完整的爬虫流程"""
        logger.info("🚀 开始运行镜像爬虫...")
        start_time = time.time()

        # 步骤1: 添加已知镜像
        self.add_known_mirrors()

        # 步骤2: 爬取网络数据
        self.crawl_github_repos()

        # 步骤3: 验证 GitHub 镜像
        self.validate_github_mirrors()

        # 步骤4: 生成数据文件
        self.generate_mirrors_json()

        # 步骤5: 生成 README
        self.generate_readme()

        end_time = time.time()
        logger.info(f"✅ 爬虫运行完成，耗时 {end_time - start_time:.2f} 秒")

def main():
    """主函数"""
    crawler = MirrorCrawler()
    crawler.run()

if __name__ == "__main__":
    main()
