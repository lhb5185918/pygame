#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import datetime

class 青岛地图系统:
    """青岛地图系统，管理青岛市各个区域、地标和交通方式"""
    
    def __init__(self):
        """初始化青岛地图系统"""
        # 记录已探索的区域
        self.已探索区域 = set()
        # 记录已乘坐的交通工具
        self.已乘坐交通 = set()
        # 记录方言熟练度 (0-100)
        self.方言熟练度 = 0
        # 记录最后访问的区域
        self.当前区域 = "市南区"
        # 定义区域数据
        self.区域数据 = {
            # 市南区 (老城区)
            "市南区": {
                "描述": "青岛最繁华的中心城区，拥有众多殖民时期建筑和海滨风光",
                "地标": ["栈桥", "八大关", "小鱼山", "五四广场", "奥帆中心", "天主教堂", "基督教堂"],
                "特产": ["啤酒", "海鲜", "崂山矿泉水"],
                "交通": ["1路公交车", "26路公交车", "出租车", "有轨电车"],
                "年代变化": {
                    "1996-2000": {
                        "描述": "老城区风貌，游客较少，栈桥附近商业不发达",
                        "地标": ["栈桥", "八大关", "小鱼山", "天主教堂", "基督教堂"],
                        "交通": ["1路公交车", "26路公交车", "出租车", "有轨电车"]
                    },
                    "2001-2005": {
                        "描述": "市区改造初期，城市面貌逐渐更新，游客增多",
                        "地标": ["栈桥", "八大关", "小鱼山", "天主教堂", "基督教堂", "海底世界"],
                        "交通": ["1路公交车", "26路公交车", "出租车", "有轨电车"]
                    },
                    "2006-2010": {
                        "描述": "奥运会帆船比赛举办地，城市面貌焕然一新",
                        "地标": ["栈桥", "八大关", "小鱼山", "五四广场", "奥帆中心", "天主教堂", "基督教堂"],
                        "交通": ["1路公交车", "26路公交车", "出租车", "有轨电车", "观光巴士"]
                    }
                },
                "方言样例": ["老师傅，去栈桥得多钱啊？", "这个鱼丸长得真讲究"]
            },
            # 市北区
            "市北区": {
                "描述": "青岛的传统工业区和商业区，拥有台东商业区和海泊河等",
                "地标": ["台东步行街", "即墨路小商品市场", "宁夏路小吃街", "海泊河公园"],
                "特产": ["麻花", "煎饼果子", "焖子"],
                "交通": ["5路公交车", "231路公交车", "出租车"],
                "年代变化": {
                    "1996-2000": {
                        "描述": "工业区色彩浓厚，台东商业区是传统购物场所",
                        "地标": ["台东步行街", "即墨路小商品市场", "劳动公园"],
                        "交通": ["5路公交车", "26路公交车", "出租车"]
                    },
                    "2001-2005": {
                        "描述": "市北区开始改造，传统工业逐渐外迁",
                        "地标": ["台东步行街", "即墨路小商品市场", "宁夏路小吃街", "劳动公园"],
                        "交通": ["5路公交车", "231路公交车", "出租车"]
                    },
                    "2006-2010": {
                        "描述": "传统工业基本外迁，居住和商业功能增强",
                        "地标": ["台东步行街", "即墨路小商品市场", "宁夏路小吃街", "海泊河公园", "劳动公园"],
                        "交通": ["5路公交车", "231路公交车", "出租车", "观光巴士"]
                    }
                },
                "方言样例": ["去台东啊，坐5路车就行", "这个煎饼果子卷俩鸡蛋"]
            },
            # 四方区（2010年后并入市北区）
            "四方区": {
                "描述": "青岛的铁路枢纽和传统工业区，四方机车车辆厂所在地",
                "地标": ["四方火车站", "四方机车车辆厂", "杭州路商业街"],
                "特产": ["四方蒸饺", "铁路文化纪念品"],
                "交通": ["9路公交车", "27路公交车", "火车"],
                "年代变化": {
                    "1996-2000": {
                        "描述": "传统工业区，火车站是重要交通枢纽",
                        "地标": ["四方火车站", "四方机车车辆厂"],
                        "交通": ["9路公交车", "27路公交车", "火车"]
                    },
                    "2001-2005": {
                        "描述": "区域功能多元化，商业逐渐发展",
                        "地标": ["四方火车站", "四方机车车辆厂", "杭州路商业街"],
                        "交通": ["9路公交车", "27路公交车", "火车"]
                    },
                    "2006-2010": {
                        "描述": "行政区划调整前夕，与市北区联系加强",
                        "地标": ["四方火车站", "四方机车车辆厂", "杭州路商业街", "四方公园"],
                        "交通": ["9路公交车", "27路公交车", "火车", "12路大巴"]
                    }
                },
                "方言样例": ["去四方火车站坐几路车啊？", "车厂门口的蒸饺可好吃嘞"]
            },
            # 李沧区
            "李沧区": {
                "描述": "青岛的东部新区，兼具居住和商业功能",
                "地标": ["李村大集", "振华购物中心", "李沧公园", "九水路夜市"],
                "特产": ["煎饼卷大葱", "锅贴", "鲅鱼水饺"],
                "交通": ["304路公交车", "219路公交车", "出租车"],
                "年代变化": {
                    "1996-2000": {
                        "描述": "相对较为偏远的居住区，李村大集是重要的民俗集市",
                        "地标": ["李村大集", "李沧公园"],
                        "交通": ["304路公交车", "25路公交车"]
                    },
                    "2001-2005": {
                        "描述": "区域建设加快，商业设施增多",
                        "地标": ["李村大集", "振华购物中心", "李沧公园"],
                        "交通": ["304路公交车", "219路公交车", "出租车"]
                    },
                    "2006-2010": {
                        "描述": "城市东扩的重要区域，高层建筑增多",
                        "地标": ["李村大集", "振华购物中心", "李沧公园", "九水路夜市", "万达广场"],
                        "交通": ["304路公交车", "219路公交车", "出租车", "地铁3号线(规划中)"]
                    }
                },
                "方言样例": ["今儿李村大集，咱去赶赶集", "这煎饼馃子卷大葱可香啦"]
            },
            # 崂山区
            "崂山区": {
                "描述": "青岛东部的山海风景区，崂山道教文化中心",
                "地标": ["崂山风景区", "石老人海水浴场", "中国海洋大学", "松岭路啤酒街"],
                "特产": ["崂山道茶", "崂山矿泉水", "海鲜"],
                "交通": ["104路公交车", "304路公交车", "旅游专线"],
                "年代变化": {
                    "1996-2000": {
                        "描述": "较为偏远的风景区和郊区，旅游设施简单",
                        "地标": ["崂山风景区", "石老人海水浴场"],
                        "交通": ["104路公交车", "旅游专线"]
                    },
                    "2001-2005": {
                        "描述": "旅游开发初具规模，大学城建设启动",
                        "地标": ["崂山风景区", "石老人海水浴场", "中国海洋大学"],
                        "交通": ["104路公交车", "304路公交车", "旅游专线"]
                    },
                    "2006-2010": {
                        "描述": "成为城市东部新区，高校和科技园区发展迅速",
                        "地标": ["崂山风景区", "石老人海水浴场", "中国海洋大学", "松岭路啤酒街", "青岛啤酒博物馆"],
                        "交通": ["104路公交车", "304路公交车", "旅游专线", "隧道快速路"]
                    }
                },
                "方言样例": ["上崂山得坐旅游车", "石老人那边海水可干净啦"]
            },
            # 黄岛区（原胶南市）
            "黄岛区": {
                "描述": "青岛西部的工业新区和港口，隔海相望",
                "地标": ["金沙滩", "董家口港", "黄岛油库", "薛家岛"],
                "特产": ["海产品", "农家乐", "开发区特色小吃"],
                "交通": ["隧道巴士", "801路公交车", "轮渡", "胶黄铁路"],
                "年代变化": {
                    "1996-2000": {
                        "描述": "远离市区的工业港口区，交通不便",
                        "地标": ["黄岛油库", "前湾港"],
                        "交通": ["801路公交车", "轮渡"]
                    },
                    "2001-2005": {
                        "描述": "开发区建设加速，旅游资源初步开发",
                        "地标": ["金沙滩", "董家口港", "黄岛油库"],
                        "交通": ["801路公交车", "轮渡", "胶黄铁路"]
                    },
                    "2006-2010": {
                        "描述": "西海岸新区崛起，成为青岛新的经济增长极",
                        "地标": ["金沙滩", "董家口港", "黄岛油库", "薛家岛", "青岛经济技术开发区"],
                        "交通": ["隧道巴士", "801路公交车", "轮渡", "胶黄铁路"]
                    }
                },
                "方言样例": ["去黄岛坐轮渡最快", "金沙滩的沙子比大沙滩的好"]
            }
        }
        
        # 定义交通方式及其费用
        self.交通费用 = {
            "1路公交车": 1,
            "5路公交车": 1,
            "9路公交车": 1,
            "12路大巴": 2,
            "25路公交车": 1,
            "26路公交车": 1,
            "27路公交车": 1,
            "104路公交车": 2,
            "219路公交车": 1,
            "231路公交车": 1,
            "304路公交车": 2,
            "801路公交车": 3,
            "出租车": 10,
            "有轨电车": 2,
            "观光巴士": 5,
            "火车": 8,
            "轮渡": 10,
            "隧道巴士": 15,
            "旅游专线": 8,
            "胶黄铁路": 12,
            "隧道快速路": 20
        }
        
        # 区域之间的可达性
        self.区域连接 = {
            "市南区": ["市北区", "四方区", "崂山区"],
            "市北区": ["市南区", "四方区", "李沧区"],
            "四方区": ["市北区", "李沧区"],
            "李沧区": ["市北区", "四方区", "崂山区"],
            "崂山区": ["市南区", "李沧区"],
            "黄岛区": ["市南区"]  # 只能通过轮渡或隧道从市南区到达
        }
        
        # 方言词典
        self.方言词典 = {
            "地图": "舆图",
            "公共汽车": "公共",
            "去": "蹿",
            "很好": "挺讲究",
            "非常": "老",
            "吃饭": "造饭",
            "看": "瞅",
            "走": "撒丫子",
            "说话": "唠嗑",
            "朋友": "哥们",
            "钱": "票子",
            "便宜": "掉价",
            "贵": "盘",
            "漂亮": "齐整"
        }
        
        # ASCII艺术地标
        self.地标ASCII艺术 = {
            "栈桥": """
         _____
        |     |
  ~~~~~~~~~~~~~~~~~~~~~
     ~~~~~~~~~~~~~~~~~
       ~~~~~~~~~~~~~~
         ~~~~~~~~~~
            ~~~~
            """,
            "崂山风景区": """
              /\\
             /  \\
            /    \\
           /      \\
          /        \\
         /          \\
        /            \\
       /              \\
      /                \\
     /                  \\
    /____________________\\
            """,
            "五四广场": """
            ___
           |   |
           |___|
         /       \\
        /         \\
       |           |
       |    五四    |
       |    广场    |
       |           |
        \\         /
         \\_______/
            """
        }
    
    def 获取所有区域(self, 年代范围=None):
        """获取所有可用区域
        
        参数:
            年代范围(str): 年代范围，如'1996-2000'
            
        返回:
            list: 区域列表
        """
        区域列表 = list(self.区域数据.keys())
        
        # 根据年代返回可用区域
        if 年代范围 == '1996-2000' or 年代范围 == '2001-2005' or 年代范围 == '2006-2010':
            # 2010年后四方区并入市北区，但在这个年代范围还存在
            return 区域列表
        else:
            # 默认返回当前区域（移除四方区）
            return [区域 for 区域 in 区域列表 if 区域 != "四方区"]
    
    def 获取区域信息(self, 区域名, 年代范围=None):
        """获取区域详细信息
        
        参数:
            区域名(str): 区域名称
            年代范围(str): 年代范围，如'1996-2000'
            
        返回:
            dict: 区域信息
        """
        if 区域名 not in self.区域数据:
            return None
            
        区域信息 = self.区域数据[区域名].copy()
        
        # 根据年代返回相应的信息
        if 年代范围 and 年代范围 in 区域信息["年代变化"]:
            年代信息 = 区域信息["年代变化"][年代范围]
            区域信息["描述"] = 年代信息["描述"]
            区域信息["地标"] = 年代信息["地标"]
            区域信息["交通"] = 年代信息["交通"]
            
        # 标记已探索
        self.已探索区域.add(区域名)
        self.当前区域 = 区域名
        
        return 区域信息
    
    def 移动到区域(self, 目标区域, 交通方式, 年代范围=None):
        """从当前区域移动到目标区域
        
        参数:
            目标区域(str): 目标区域名称
            交通方式(str): 选择的交通方式
            年代范围(str): 年代范围，如'1996-2000'
            
        返回:
            dict: 包含成功与否、消息和花费
        """
        # 检查目标区域是否存在
        if 目标区域 not in self.区域数据:
            return {"成功": False, "消息": f"目标区域 {目标区域} 不存在"}
            
        # 检查在当前年代是否可达
        可用区域 = self.获取所有区域(年代范围)
        if 目标区域 not in 可用区域:
            return {"成功": False, "消息": f"在{年代范围}年代，{目标区域}尚不可达"}
            
        # 检查区域连接性
        if 目标区域 != self.当前区域 and 目标区域 not in self.区域连接.get(self.当前区域, []):
            return {"成功": False, "消息": f"无法直接从{self.当前区域}到达{目标区域}"}
            
        # 检查交通方式是否可用
        目标区域信息 = self.获取区域信息(目标区域, 年代范围)
        if 交通方式 not in 目标区域信息["交通"]:
            return {"成功": False, "消息": f"{交通方式}在{年代范围}年代不可用于前往{目标区域}"}
            
        # 计算交通费用
        费用 = self.交通费用.get(交通方式, 5)  # 默认5元
        
        # 记录已使用的交通方式
        self.已乘坐交通.add(交通方式)
        
        # 更新当前区域
        self.当前区域 = 目标区域
        
        return {
            "成功": True,
            "消息": f"成功使用{交通方式}到达{目标区域}",
            "花费": 费用
        }
    
    def 获取ASCII艺术(self, 地标名):
        """获取地标的ASCII艺术
        
        参数:
            地标名(str): 地标名称
            
        返回:
            str: ASCII艺术字符串
        """
        return self.地标ASCII艺术.get(地标名, "该地标暂无ASCII艺术图案")
    
    def 获取区域之间的交通方式(self, 起始区域, 目标区域, 年代范围=None):
        """获取从起始区域到目标区域的可用交通方式
        
        参数:
            起始区域(str): 起始区域名称
            目标区域(str): 目标区域名称
            年代范围(str): 年代范围，如'1996-2000'
            
        返回:
            list: 可用交通方式列表
        """
        # 检查区域连接性
        if 目标区域 not in self.区域连接.get(起始区域, []):
            return []
            
        # 获取两个区域在当前年代的交通方式
        起始区域信息 = self.获取区域信息(起始区域, 年代范围)
        目标区域信息 = self.获取区域信息(目标区域, 年代范围)
        
        if not 起始区域信息 or not 目标区域信息:
            return []
            
        # 获取交集
        可用交通 = set(起始区域信息["交通"]) & set(目标区域信息["交通"])
        return list(可用交通)
    
    def 获取方言样例(self, 区域名=None):
        """获取特定区域或随机区域的方言样例
        
        参数:
            区域名(str): 区域名称，如果为None则随机选择
            
        返回:
            str: 方言样例
        """
        if not 区域名:
            区域名 = random.choice(list(self.区域数据.keys()))
            
        if 区域名 in self.区域数据 and "方言样例" in self.区域数据[区域名]:
            return random.choice(self.区域数据[区域名]["方言样例"])
        else:
            return "这个地方没有特别的方言样例"
    
    def 方言互动(self, 原文本):
        """根据方言熟练度转换标准文本为方言文本
        
        参数:
            原文本(str): 原始文本
            
        返回:
            str: 转换后的文本
        """
        # 根据方言熟练度决定替换比例
        替换概率 = min(self.方言熟练度 / 100.0, 0.8)  # 最高80%替换率
        
        结果文本 = 原文本
        for 标准词, 方言词 in self.方言词典.items():
            if 标准词 in 结果文本 and random.random() < 替换概率:
                结果文本 = 结果文本.replace(标准词, 方言词)
                
        return 结果文本
    
    def 提高方言熟练度(self, 增加值=5):
        """提高方言熟练度
        
        参数:
            增加值(int): 要增加的熟练度
            
        返回:
            int: 增加后的熟练度
        """
        self.方言熟练度 = min(100, self.方言熟练度 + 增加值)
        return self.方言熟练度
    
    def 获取方言熟练度描述(self):
        """根据方言熟练度获取描述
        
        返回:
            str: 熟练度描述
        """
        if self.方言熟练度 < 20:
            return "外地人，完全听不懂青岛话"
        elif self.方言熟练度 < 40:
            return "初来乍到，能听懂几个常用词"
        elif self.方言熟练度 < 60:
            return "小半年青岛生活，勉强能听懂日常对话"
        elif self.方言熟练度 < 80:
            return "老青岛，说起青岛话来有模有样"
        else:
            return "纯正青岛本地人，地道青岛话脱口而出"
    
    def 访问地标(self, 区域名, 地标名, 年代范围=None):
        """访问特定区域的地标
        
        参数:
            区域名(str): 区域名称
            地标名(str): 地标名称
            年代范围(str): 年代范围，如'1996-2000'
            
        返回:
            dict: 访问结果
        """
        区域信息 = self.获取区域信息(区域名, 年代范围)
        
        if not 区域信息:
            return {"成功": False, "消息": f"区域 {区域名} 不存在"}
            
        if 地标名 not in 区域信息["地标"]:
            return {"成功": False, "消息": f"{地标名} 在{年代范围}年代的{区域名}不存在"}
            
        # 获取地标的ASCII艺术
        地标艺术 = self.获取ASCII艺术(地标名)
        
        # 根据地标生成描述
        描述 = self.获取地标描述(地标名, 年代范围)
        
        return {
            "成功": True,
            "消息": f"参观了{区域名}的{地标名}",
            "描述": 描述,
            "ASCII艺术": 地标艺术
        }
    
    def 获取地标描述(self, 地标名, 年代范围=None):
        """获取地标在特定年代的描述
        
        参数:
            地标名(str): 地标名称
            年代范围(str): 年代范围，如'1996-2000'
            
        返回:
            str: 地标描述
        """
        地标描述 = {
            "栈桥": {
                "1996-2000": "青岛的标志性景点，木质栈桥延伸入海，游客不多，附近小商贩兜售海鲜和纪念品。",
                "2001-2005": "栈桥周边开始商业化，游客增多，增设了观光设施和商店。",
                "2006-2010": "奥运会前后经过翻修，游客众多，成为热门旅游打卡地。"
            },
            "八大关": {
                "1996-2000": "安静的花园式别墅区，住着一些老干部，建筑保存良好但不对外开放。",
                "2001-2005": "部分开放参观，游客可以沿着林荫道漫步，部分别墅院子可以进入。",
                "2006-2010": "成为景区，有导游讲解各国建筑风格，游客络绎不绝。"
            },
            "崂山风景区": {
                "1996-2000": "自然风景区，道教圣地，设施简陋，交通不便，主要有登山步道和几个道观。",
                "2001-2005": "开始规范化管理，设立游客中心，修建了较好的登山步道和休息设施。",
                "2006-2010": "完全商业化的景区，索道、游客中心、停车场一应俱全，成为5A级景区。"
            },
            "五四广场": {
                "2006-2010": "为纪念五四运动而建的现代化城市广场，风帆雕塑巍然矗立，周边高楼林立，夜景绚丽。"
            }
        }
        
        if 地标名 in 地标描述 and 年代范围 in 地标描述[地标名]:
            return 地标描述[地标名][年代范围]
        else:
            return f"{地标名}是青岛的著名地标。"
    
    def 购买特产(self, 区域名, 特产名):
        """在特定区域购买特产
        
        参数:
            区域名(str): 区域名称
            特产名(str): 特产名称
            
        返回:
            dict: 购买结果
        """
        区域信息 = self.获取区域信息(区域名)
        
        if not 区域信息:
            return {"成功": False, "消息": f"区域 {区域名} 不存在"}
            
        if 特产名 not in 区域信息["特产"]:
            return {"成功": False, "消息": f"{特产名} 不是{区域名}的特产"}
            
        # 特产价格
        特产价格 = {
            "啤酒": 3,
            "海鲜": 50,
            "崂山矿泉水": 2,
            "麻花": 5,
            "煎饼果子": 3,
            "焖子": 8,
            "四方蒸饺": 6,
            "铁路文化纪念品": 20,
            "煎饼卷大葱": 4,
            "锅贴": 6,
            "鲅鱼水饺": 12,
            "崂山道茶": 80,
            "海产品": 30,
            "农家乐": 100
        }
        
        价格 = 特产价格.get(特产名, 10)  # 默认10元
        
        return {
            "成功": True,
            "消息": f"成功在{区域名}购买了{特产名}",
            "花费": 价格,
            "物品": 特产名
        }
    
    def 获取已探索区域列表(self):
        """获取已探索的区域列表
        
        返回:
            list: 已探索区域列表
        """
        return list(self.已探索区域)
    
    def 获取已乘坐交通列表(self):
        """获取已乘坐的交通工具列表
        
        返回:
            list: 已乘坐交通工具列表
        """
        return list(self.已乘坐交通) 