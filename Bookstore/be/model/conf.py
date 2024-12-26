# 数据库配置
DB_CONFIG = {
    # PostgreSQL配置 - 用于核心数据
    'postgres': {
        'database': 'bookstore',                # 数据库名
        'user': 'ecnu10225501402',             # PostgreSQL用户名
        'password': 'ECNU10225501402',         # PostgreSQL密码
        'host': 'localhost',                    # 数据库地址
        'port': '5432'                         # PostgreSQL默认端口
    },
    
    # MongoDB配置 - 用于Blob数据
    'mongo': {
        # MongoDB连接URI，包含认证信息
        'uri': 'mongodb://ecnu10225501402:ECNU10225501402@localhost:27017/',
        'database': 'bookstore'
    }
} 