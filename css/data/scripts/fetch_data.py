#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import feedparser
import datetime
import os
import re
from bs4 import BeautifulSoup

# 创建数据目录（如果不存在） 
os.makedirs('data', exist_ok=True)

# 初始化数据结构
data = {
    "lastUpdated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "nextUpdate": (datetime.datetime.now() + datetime.timedelta(days=1)).replace(hour=8, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
    "counts": {
        "academic": 0,
        "clinical": 0,
        "policy": 0
    },
    "latest": {
        "academic": [],
        "clinical": [],
        "policy": []
    }
}

# 获取学术研究数据
def fetch_academic_research():
    print("获取学术研究数据...")
    academic_items = []
    
    # 从PubMed获取数据
    pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/rss/search/1lYixSZLGOzU9hM/?limit=10&utm_campaign=pubmed-2&fc=20210111085146"
    try:
        feed = feedparser.parse(pubmed_url) 
        for entry in feed.entries[:5]:  # 获取最新5条
            date_obj = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
            item = {
                "date": date_obj.strftime("%Y-%m-%d"),
                "title": entry.title,
                "source": "PubMed",
                "link": entry.link
            }
            academic_items.append(item)
    except Exception as e:
        print(f"获取PubMed数据出错: {e}")
    
    # 从Nature获取数据
    nature_url = "https://www.nature.com/search.rss?q=stem+cell+OR+immune+cell+therapy&date_range=last_7_days&order=relevance"
    try:
        feed = feedparser.parse(nature_url) 
        for entry in feed.entries[:5]:  # 获取最新5条
            date_obj = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
            item = {
                "date": date_obj.strftime("%Y-%m-%d"),
                "title": entry.title,
                "source": "Nature",
                "link": entry.link
            }
            academic_items.append(item)
    except Exception as e:
        print(f"获取Nature数据出错: {e}")
    
    # 按日期排序并取最新的10条
    academic_items.sort(key=lambda x: x["date"], reverse=True)
    data["latest"]["academic"] = academic_items[:10]
    data["counts"]["academic"] = len(academic_items)
    
    print(f"获取到 {len(academic_items)} 条学术研究数据")

# 获取临床试验数据
def fetch_clinical_trials():
    print("获取临床试验数据...")
    clinical_items = []
    
    # 从ClinicalTrials.gov获取数据
    ct_url = "https://clinicaltrials.gov/ct2/results/rss.xml?rcv_d=30&lup_d=30&term=stem+cell+OR+immune+cell+therapy&type=Intr&cntry=CN&cntry=US&count=10"
    try:
        feed = feedparser.parse(ct_url) 
        for entry in feed.entries:
            # 提取试验ID
            trial_id_match = re.search(r'NCT\d+', entry.link)
            trial_id = trial_id_match.group(0) if trial_id_match else ""
            
            # 提取日期
            date_obj = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
            
            item = {
                "date": date_obj.strftime("%Y-%m-%d"),
                "title": entry.title,
                "trialId": trial_id,
                "link": entry.link
            }
            clinical_items.append(item)
    except Exception as e:
        print(f"获取ClinicalTrials.gov数据出错: {e}")
    
    # 按日期排序并取最新的10条
    clinical_items.sort(key=lambda x: x["date"], reverse=True)
    data["latest"]["clinical"] = clinical_items[:10]
    data["counts"]["clinical"] = len(clinical_items)
    
    print(f"获取到 {len(clinical_items)} 条临床试验数据")

# 获取政策监控数据
def fetch_policy_updates():
    print("获取政策监控数据...")
    policy_items = []
    
    # 从国家药监局获取数据
    try:
        nmpa_url = "https://www.nmpa.gov.cn/directory/web/nmpa/rss/ypjgdt.xml"
        feed = feedparser.parse(nmpa_url) 
        
        for entry in feed.entries[:10]:
            # 检查是否与细胞治疗相关
            keywords = ["干细胞", "免疫细胞", "细胞治疗", "基因治疗", "CAR-T"]
            if any(keyword in entry.title or keyword in entry.description for keyword in keywords):
                date_obj = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
                item = {
                    "date": date_obj.strftime("%Y-%m-%d"),
                    "title": entry.title,
                    "agency": "国家药监局",
                    "link": entry.link
                }
                policy_items.append(item)
    except Exception as e:
        print(f"获取国家药监局数据出错: {e}")
    
    # 从FDA获取数据
    try:
        fda_url = "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/drugs/rss.xml"
        feed = feedparser.parse(fda_url) 
        
        for entry in feed.entries[:10]:
            # 检查是否与细胞治疗相关
            keywords = ["stem cell", "immune cell", "cell therapy", "gene therapy", "CAR-T"]
            if any(keyword in entry.title.lower() or keyword in entry.description.lower() for keyword in keywords):
                date_obj = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
                item = {
                    "date": date_obj.strftime("%Y-%m-%d"),
                    "title": entry.title,
                    "agency": "FDA",
                    "link": entry.link
                }
                policy_items.append(item)
    except Exception as e:
        print(f"获取FDA数据出错: {e}")
    
    # 按日期排序并取最新的10条
    policy_items.sort(key=lambda x: x["date"], reverse=True)
    data["latest"]["policy"] = policy_items[:10]
    data["counts"]["policy"] = len(policy_items)
    
    print(f"获取到 {len(policy_items)} 条政策监控数据")

# 主函数
def main():
    print("开始获取数据...")
    
    # 获取各类数据
    fetch_academic_research()
    fetch_clinical_trials()
    fetch_policy_updates()
    
    # 保存数据到JSON文件
    with open('data/latest.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("数据获取完成，已保存到 data/latest.json")

if __name__ == "__main__":
    main()
