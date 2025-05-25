#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试主爬虫功能
"""

import os
import json
import subprocess
import sys

def test_main_crawler():
    """测试主爬虫功能"""
    print("🧪 开始测试主爬虫...")
    
    # 运行主爬虫
    try:
        result = subprocess.run([sys.executable, "main_crawler.py"], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 主爬虫运行成功")
        else:
            print("❌ 主爬虫运行失败")
            print(f"错误输出: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ 主爬虫运行超时")
        return False
    except Exception as e:
        print(f"❌ 运行主爬虫时出错: {e}")
        return False
    
    # 检查生成的文件
    files_to_check = ["mirrors.json", "README.md"]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file_path} 存在 ({file_size} bytes)")
        else:
            print(f"❌ {file_path} 不存在")
            return False
    
    # 验证 JSON 格式
    try:
        with open("mirrors.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 检查必要的字段
        required_fields = ["update_time", "github_mirrors", "docker_mirrors"]
        for field in required_fields:
            if field not in data:
                print(f"❌ mirrors.json 缺少字段: {field}")
                return False
        
        github_count = data["github_mirrors"]["count"]
        docker_count = data["docker_mirrors"]["count"]
        
        print(f"📊 GitHub 镜像数量: {github_count}")
        print(f"📊 Docker 镜像数量: {docker_count}")
        
        if github_count > 0 and docker_count > 0:
            print("✅ 镜像数据验证通过")
        else:
            print("⚠️ 镜像数量为 0，可能存在问题")
            
    except json.JSONDecodeError:
        print("❌ mirrors.json 格式无效")
        return False
    except Exception as e:
        print(f"❌ 验证 mirrors.json 时出错: {e}")
        return False
    
    print("✅ 所有测试通过!")
    return True

if __name__ == "__main__":
    success = test_main_crawler()
    sys.exit(0 if success else 1)
