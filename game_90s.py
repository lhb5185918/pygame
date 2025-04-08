#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import random
import time
try:
    import curses
except ImportError:
    print("警告：未找到curses库，在Windows上可能需要安装windows-curses")
    print("尝试：pip install windows-curses")

try:
    import pygame
except ImportError:
    print("警告：未找到pygame库，音效功能不可用")
    print("尝试：pip install pygame")

class 九零后时光机:
    def __init__(self):
        self.玩家名字 = ""
        self.当前年份 = 1996
        self.当前章节 = "小学一年级"
        self.属性 = {
            "学业值": 50,
            "零花钱": 20,
            "家庭关系": 80,
            "健康值": 90,
            "爱国值": 60,
            "人际关系": 50
        }
        self.收藏品 = []
        self.已触发事件 = []
        self.历史选择 = {}
        
    def 保存游戏(self):
        with open(f"{self.玩家名字}_存档.pkl", "wb") as f:
            pickle.dump(self, f)
        print(f"游戏已保存 - {self.玩家名字}的{self.当前年份}年生活")
    
    def 加载游戏(self, 存档名):
        try:
            with open(存档名, "rb") as f:
                loaded_game = pickle.load(f)
                self.__dict__.update(loaded_game.__dict__)
            print(f"欢迎回来，{self.玩家名字}！现在是{self.当前年份}年")
            return True
        except FileNotFoundError:
            print("存档未找到")
            return False
    
    def 开始新游戏(self):
        self.显示ASCII艺术("""
        ╭──────────────────────────────╮
        │       九零后时光机           │
        │   - 重返那些年的日子 -       │
        ╰──────────────────────────────╯
        """)
        self.玩家名字 = input("请输入你的名字: ")
        print(f"你好，{self.玩家名字}！欢迎回到1996年...")
        time.sleep(1)
        print("那时的你，正坐在小学一年级的教室里...")
        time.sleep(1)
        self.主菜单()
    
    def 显示ASCII艺术(self, 文本):
        # 简单实现，未来可以使用curses库增强
        print(文本)
    
    def 播放音效(self, 音效名):
        # pygame音效系统，未来实现
        pass
    
    def 属性变化(self, 属性名, 变化值):
        self.属性[属性名] += 变化值
        # 确保属性值在0-100之间
        self.属性[属性名] = max(0, min(100, self.属性[属性名]))
        变化描述 = "增加" if 变化值 > 0 else "减少"
        print(f"{属性名}{变化描述}了{abs(变化值)}点 (当前值: {self.属性[属性名]})")
    
    def 触发事件(self, 年份):
        # 根据年份触发对应事件
        历史事件表 = {
            1997: ["香港回归晚会转播", "电脑房《红色警戒》对战", "收集水浒卡社交事件"],
            2003: ["非典停课在家看《流星花园》", "父母下岗危机", "初代淘宝网购体验"],
            # 可以继续添加其他年份的事件
        }
        
        if 年份 in 历史事件表:
            可用事件 = [事件 for 事件 in 历史事件表[年份] if 事件 not in self.已触发事件]
            if 可用事件:
                当前事件 = random.choice(可用事件)
                self.已触发事件.append(当前事件)
                self.处理事件(当前事件)
    
    def 处理事件(self, 事件名):
        print(f"\n【历史事件】: {事件名}")
        
        # 事件逻辑
        if 事件名 == "香港回归晚会转播":
            print("1997年，香港回归的盛大庆典在电视上播出，全家人围坐在电视机前观看。")
            选择 = self.提供选择(["认真观看并努力理解意义", "觉得无聊想去玩", "问父母有关香港的问题"])
            
            if 选择 == 1:
                print("你被庄严的仪式深深吸引，对祖国多了一份认同感。")
                self.属性变化("爱国值", 10)
            elif 选择 == 2:
                print("你溜出去玩了，错过了这一历史时刻。")
                self.属性变化("爱国值", -5)
            else:
                print("父母耐心地解释了香港的历史，你懂得了更多。")
                self.属性变化("爱国值", 8)
                self.属性变化("家庭关系", 5)
        
        # 可以继续添加更多事件的处理逻辑
    
    def 提供选择(self, 选项列表):
        print("\n做出你的选择:")
        for i, 选项 in enumerate(选项列表, 1):
            print(f"{i}. {选项}")
        
        while True:
            try:
                选择 = int(input("输入选项编号: "))
                if 1 <= 选择 <= len(选项列表):
                    return 选择
                else:
                    print("无效选择，请重试")
            except ValueError:
                print("请输入数字")
    
    def 时间推进(self):
        self.当前年份 += 1
        # 根据年份确定学年
        年龄 = self.当前年份 - 1990  # 假设90后出生于1990年
        
        if 6 <= 年龄 <= 11:
            年级 = 年龄 - 5
            self.当前章节 = f"小学{年级}年级"
        elif 12 <= 年龄 <= 14:
            年级 = 年龄 - 11
            self.当前章节 = f"初中{年级}年级"
        elif 15 <= 年龄 <= 17:
            年级 = 年龄 - 14
            self.当前章节 = f"高中{年级}年级"
        elif 年龄 >= 18:
            self.当前章节 = "大学或工作"
        
        print(f"\n时光机启动...\n年份推进到: {self.当前年份}年")
        print(f"当前章节: {self.当前章节}")
        self.触发事件(self.当前年份)
    
    def 主菜单(self):
        while True:
            print(f"\n【九零后时光机】 - {self.玩家名字}的{self.当前年份}年")
            print(f"当前章节: {self.当前章节}")
            print("1. 探索当前时间")
            print("2. 查看个人属性")
            print("3. 查看收藏品")
            print("4. 时间推进")
            print("5. 保存游戏")
            print("6. 退出游戏")
            
            选择 = input("请选择: ")
            
            if 选择 == "1":
                self.探索当前时间()
            elif 选择 == "2":
                self.显示属性()
            elif 选择 == "3":
                self.显示收藏品()
            elif 选择 == "4":
                self.时间推进()
            elif 选择 == "5":
                self.保存游戏()
            elif 选择 == "6":
                print("感谢游玩《九零后时光机》！")
                break
            else:
                print("无效选择，请重试")
    
    def 探索当前时间(self):
        年代特色 = {
            1996: ["小霸王学习机热销", "《西游记》热播", "小学课间玩纸飞机"],
            1997: ["香港回归", "大哥大开始流行", "《还珠格格》第一部播出"],
            1998: ["互联网开始普及", "《大话西游》风靡", "学校发放《小学生日常行为规范》"],
            # 可继续添加
        }
        
        if self.当前年份 in 年代特色:
            print(f"\n【{self.当前年份}年的流行元素】")
            for 特色 in 年代特色[self.当前年份]:
                print(f"· {特色}")
            
            探索选项 = ["去文具店", "在家看电视", "去同学家玩", "返回"]
            选择 = self.提供选择(探索选项)
            
            if 选择 == 1:
                print("你在文具店发现了好多新奇的文具...")
                # 文具店事件
            elif 选择 == 2:
                print("电视正在播放...")
                # 电视节目事件
            elif 选择 == 3:
                print("你和同学一起玩耍...")
                # 同学互动事件
        else:
            print("这一年的记忆还不太清晰...")
    
    def 显示属性(self):
        print("\n【个人属性】")
        for 属性, 值 in self.属性.items():
            进度条 = "█" * (值 // 10) + "░" * (10 - 值 // 10)
            print(f"{属性}: {进度条} {值}/100")
    
    def 显示收藏品(self):
        if not self.收藏品:
            print("\n你还没有收集到任何宝贵的童年收藏品。")
            return
            
        print("\n【童年收藏品】")
        for i, 收藏品 in enumerate(self.收藏品, 1):
            print(f"{i}. {收藏品}")

if __name__ == "__main__":
    game = 九零后时光机()
    try:
        game.开始新游戏()
    except KeyboardInterrupt:
        print("\n游戏被中断")
    except Exception as e:
        print(f"游戏出错: {e}") 