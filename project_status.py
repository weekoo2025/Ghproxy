#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目状态检查
"""

import os
import json
from datetime import datetime

def check_project_status():
    """检查项目状态"""
    print("🔍 项目状态检查")
    print("=" * 50)
    
    # 核心文件检查
    core_files = {
        "main_crawler.py": "主爬虫脚本",
        "mirrors.json": "镜像数据文件",
        "README.md": "项目说明文档",
        "requirements.txt": "Python 依赖",
        "source_urls.txt": "数据源配置",
        ".github/workflows/update-mirrors.yml": "GitHub Actions 工作流",
        "LICENSE": "许可证文件"
    }
    
    print("\n📁 核心文件检查:")
    missing_files = []
    
    for file_path, description in core_files.items():
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {description}: {file_path} ({file_size} bytes)")
        else:
            print(f"❌ {description}: {file_path} 不存在")
            missing_files.append(file_path)
    
    # 检查镜像数据
    if os.path.exists("mirrors.json"):
        try:
            with open("mirrors.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            print(f"\n📊 镜像数据统计:")
            print(f"  GitHub 镜像: {data.get('github_mirrors', {}).get('count', 0)} 个")
            print(f"  Docker 镜像: {data.get('docker_mirrors', {}).get('count', 0)} 个")
            print(f"  更新时间: {data.get('update_time', 'Unknown')}")
            
            # 显示 GitHub 镜像列表
            github_urls = data.get('github_mirrors', {}).get('urls', [])
            if github_urls:
                print(f"\n🔥 GitHub 镜像列表:")
                for url in github_urls:
                    print(f"  - {url}")
            
            # 显示 Docker 镜像列表
            docker_urls = data.get('docker_mirrors', {}).get('urls', [])
            if docker_urls:
                print(f"\n🐳 Docker 镜像列表:")
                for url in docker_urls[:5]:  # 只显示前5个
                    print(f"  - {url}")
                if len(docker_urls) > 5:
                    print(f"  ... 还有 {len(docker_urls) - 5} 个")
            
        except Exception as e:
            print(f"❌ 读取 mirrors.json 失败: {e}")
    
    # 项目完整性评估
    completion_rate = (len(core_files) - len(missing_files)) / len(core_files) * 100
    
    print(f"\n📈 项目状态:")
    print(f"  完整性: {completion_rate:.1f}%")
    print(f"  缺失文件: {len(missing_files)} 个")
    
    if completion_rate >= 90:
        print(f"  状态: 🎉 优秀")
    elif completion_rate >= 80:
        print(f"  状态: 👍 良好")
    elif completion_rate >= 70:
        print(f"  状态: ⚠️ 一般")
    else:
        print(f"  状态: ❌ 需要改进")
    
    # 使用说明
    print(f"\n🚀 使用方法:")
    print(f"  运行爬虫: python main_crawler.py")
    print(f"  测试功能: python test_main.py")
    print(f"  检查状态: python project_status.py")
    
    print(f"\n检查完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    check_project_status()
