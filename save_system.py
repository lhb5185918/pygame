#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import datetime

class 存档系统:
    """游戏存档管理系统"""
    
    def __init__(self, 存档目录="saves"):
        """初始化存档系统
        
        参数:
            存档目录(str): 存档文件保存目录
        """
        self.存档目录 = 存档目录
        self._确保目录存在()
    
    def _确保目录存在(self):
        """确保存档目录存在"""
        if not os.path.exists(self.存档目录):
            os.makedirs(self.存档目录)
    
    def 保存游戏(self, 玩家, 存档名=None):
        """保存游戏状态
        
        参数:
            玩家(Player): 玩家对象
            存档名(str): 自定义存档名，若未指定则使用默认格式
            
        返回:
            str: 存档文件路径
        """
        self._确保目录存在()
        
        if 存档名 is None:
            当前时间 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            存档名 = f"{玩家.名字}_{当前时间}.save"
        
        存档路径 = os.path.join(self.存档目录, 存档名)
        
        with open(存档路径, "wb") as f:
            pickle.dump(玩家, f)
        
        return 存档路径
    
    def 加载游戏(self, 存档名):
        """加载游戏存档
        
        参数:
            存档名(str): 存档文件名或路径
            
        返回:
            Player: 玩家对象，加载失败则返回None
        """
        # 如果只提供文件名，添加目录路径
        if os.path.dirname(存档名) == "":
            存档路径 = os.path.join(self.存档目录, 存档名)
        else:
            存档路径 = 存档名
            
        try:
            with open(存档路径, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.PickleError) as e:
            print(f"加载存档失败: {e}")
            return None
    
    def 列出存档(self):
        """列出所有可用的存档文件
        
        返回:
            list: 存档文件信息列表，每项包含 (文件名, 修改时间, 大小)
        """
        self._确保目录存在()
        存档列表 = []
        
        for 文件名 in os.listdir(self.存档目录):
            if 文件名.endswith(".save") or 文件名.endswith(".pkl"):
                文件路径 = os.path.join(self.存档目录, 文件名)
                修改时间 = datetime.datetime.fromtimestamp(
                    os.path.getmtime(文件路径)
                ).strftime("%Y-%m-%d %H:%M:%S")
                大小 = os.path.getsize(文件路径) // 1024  # KB
                
                存档列表.append((文件名, 修改时间, 大小))
        
        # 按修改时间排序，最新的在前
        存档列表.sort(key=lambda x: os.path.getmtime(
            os.path.join(self.存档目录, x[0])
        ), reverse=True)
        
        return 存档列表
    
    def 删除存档(self, 存档名):
        """删除指定存档文件
        
        参数:
            存档名(str): 存档文件名
            
        返回:
            bool: 是否成功删除
        """
        存档路径 = os.path.join(self.存档目录, 存档名)
        
        try:
            os.remove(存档路径)
            return True
        except FileNotFoundError:
            print(f"存档文件不存在: {存档名}")
            return False
        except PermissionError:
            print(f"无权限删除文件: {存档名}")
            return False 