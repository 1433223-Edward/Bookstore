# Bookstore Backend

## 项目描述
这是一书店的后端系统，支持用户注册、登录、购买图书、搜索图书等功能。
## 技术栈
 Python 3.8+
 PostgreSQL（核心数据存储）
 MongoDB（Blob数据存储）
 Flask（Web框架）
 JWT（用户认证）
## 安装步骤
1. 克隆项目

git clone https://github.com/1433223-Edward/Bookstore.git

pip install -r requirements.txt

3. 配置数据库
- 创建PostgreSQL数据库
- 创建MongoDB数据库
- 复制`be/model/conf.py.example`为`be/model/conf.py`并填入数据库配置

4. 初始化数据库
python init_db.py

5. 运行测试
pytest

6. 运行服务
python app.py

## 项目结构
bookstore/
├── be/ # 后端代码
│ ├── model/ # 数据模型
│ └── view/ # 视图函数
├── doc/ # API文档
├── fe/ # 前端测试代码
└── test/ # 测试用例

## API文档
详见 `doc/` 目录下的文档文件。

## 测试覆盖率
运行测试覆盖率报告：
bash
pytest --cov=be --cov-report=html

## 注意事项
- 请不要提交 `conf.py` 文件
- 运行测试前请确保数据库配置正确
- 建议使用虚拟环境运行项目

## 作者
苏思源
