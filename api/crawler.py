import requests
from bs4 import BeautifulSoup
import json
import time
import re

# === 配置区域 ===
BASE_URL = "http://172.16.0.193:8088"
USERNAME = "your_username"
PASSWORD = "your_password"

class ZentaoDevDocCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL.rstrip('/')
        self.docs = []

    def login(self):
        """登录禅道以获取权限"""
        # 注意：这里模拟普通登录，因为 dev 模块通常依赖 Session 
        login_page = f"{self.base_url}/index.php?m=user&f=login"
        res = self.session.get(login_page)
        
        # 尝试通过 API token 方式或模拟表单登录
        # 鉴于你之前 token 成功了，我们先尝试把 token 放入 Cookie
        # 如果还是提示需要登录，建议在浏览器 F12 查看 zentaosid 并手动填入
        login_api = f"{self.base_url}/api.php/v1/tokens"
        payload = {"account": USERNAME, "password": PASSWORD}
        res = self.session.post(login_api, json=payload)
        if res.status_code in [200, 201]:
            token = res.json().get('token')
            self.session.headers.update({"Token": token})
            print("✅ 登录验证成功")
            return True
        return False

    def get_api_list(self):
        """从主页获取所有的 apiID"""
        list_url = f"{self.base_url}/index.php?m=dev&f=api"
        print(f"正在获取接口目录: {list_url}")
        res = self.session.get(list_url)
        
        # 使用正则或 BeautifulSoup 匹配所有的 apiID=xxx
        # 禅道的链接格式通常是 apiID=123
        ids = re.findall(r'apiID=(\d+)', res.text)
        unique_ids = sorted(list(set(ids)), key=int)
        print(f"📂 发现 {len(unique_ids)} 个接口定义")
        return unique_ids

    def parse_api_detail(self, api_id):
        """爬取单个 API 的详细信息"""
        url = f"{self.base_url}/index.php?m=dev&f=api&module=restapi&apiID={api_id}&zin=1"
        try:
            res = self.session.get(url)
            if res.status_code != 200:
                return None
            
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # 提取信息 (根据禅道界面的 HTML 结构提取)
            # 这里的提取逻辑需要根据你看到的页面源码微调
            title = soup.find('h2')
            title_text = title.get_text(strip=True) if title else f"API_{api_id}"
            
            # 提取表格中的参数、URL、请求方法等
            content = soup.get_text(separator='\n', strip=True)
            
            print(f"  - 已抓取: [{api_id}] {title_text}")
            
            return {
                "id": api_id,
                "title": title_text,
                "url": url,
                "full_content": content # 保存全文，方便后续搜索
            }
        except Exception as e:
            print(f"  - ❌ 抓取 ID {api_id} 出错: {e}")
            return None

    def run(self):
        if not self.login():
            print("❌ 登录失败，请检查账号密码")
            return

        api_ids = self.get_api_list()
        if not api_ids:
            # 如果没抓到 ID 列表，可以尝试手动给个范围进行暴力探测
            print("⚠️ 未能从目录抓取到 ID，尝试暴力探测前 50 个 ID...")
            api_ids = [str(i) for i in range(1, 51)]

        for aid in api_ids:
            data = self.parse_api_detail(aid)
            if data:
                self.docs.append(data)
            time.sleep(0.5)  # 稍微停顿，避免请求过快

        # 保存结果
        with open("zentao_dev_docs_all.json", "w", encoding="utf-8") as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=4)
        print(f"\n🎉 任务完成！共抓取 {len(self.docs)} 个接口文档，保存至 zentao_dev_docs_all.json")

if __name__ == "__main__":
    crawler = ZentaoDevDocCrawler()
    crawler.run()