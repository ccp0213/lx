"""SmartVoyage 配置。本地默认值适用于 start_all.py；Docker 通过环境变量覆盖。"""

import os

from dotenv import load_dotenv

project_root = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(project_root, ".env"), override=False)
env = os.getenv("APP_ENV", "local")


class Config:
    def __init__(self):
        deepseek_key = (os.getenv("DEEPSEEK_API_KEY") or "").strip()
        provider = (os.getenv("LLM_PROVIDER") or "").strip().lower()
        if not provider:
            provider = "deepseek" if deepseek_key else "dashscope"

        if provider == "deepseek" and not deepseek_key:
            # 未填 DeepSeek Key 时回退通义，避免服务起不来
            provider = "dashscope"
            os.environ.pop("LLM_BASE_URL", None)  # 避免沿用 deepseek 的 base_url

        self.llm_provider = provider

        if self.llm_provider == "deepseek":
            self.api_key = deepseek_key
            self.base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
            self.model_name = os.getenv("LLM_MODEL_NAME", "deepseek-v4-pro")
        else:
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            env_base = (os.getenv("LLM_BASE_URL") or "").strip()
            if env_base and "deepseek" not in env_base.lower():
                self.base_url = env_base
            else:
                self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            model = os.getenv("LLM_MODEL_NAME", "qwen-plus")
            if "deepseek" in model.lower():
                model = "qwen-plus"
            self.model_name = model

        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.1"))
        self.llm_streaming = os.getenv("LLM_STREAMING", "1").strip() not in (
            "0",
            "false",
            "False",
        )

        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.port = int(os.getenv("MYSQL_PORT", "3306"))
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "123456")
        self.database = os.getenv("MYSQL_DATABASE", "travel_rag")

        self.log_file = os.getenv(
            "LOG_FILE", os.path.join(project_root, "logs", "app.log")
        )

        self.intent = {
            "weather": "WeatherQueryAssistant",
            "flight": "TicketAssistant",
            "train": "TicketAssistant",
            "concert": "TicketAssistant",
            "order": "TicketAssistant",
            "car_rental": "TripAssistant",
            "tour_group": "TripAssistant",
            "insurance": "TripAssistant",
            "trip_order": "TripAssistant",
        }

        self.weather_source = os.getenv("WEATHER_SOURCE", "api")
        self.weather_api_key = os.getenv(
            "HEFENG_WEATHER_API_KEY", "06281a98907b4aaf902bb4866552f18a"
        )
        self.weather_base_url = os.getenv(
            "WEATHER_BASE_URL",
            "https://ng5g7ercrv.re.qweatherapi.com/v7/weather/30d",
        )
        self.weather_api_host = os.getenv(
            "WEATHER_API_HOST", "ng5g7ercrv.re.qweatherapi.com"
        )
        self.weather_timezone = os.getenv("WEATHER_TIMEZONE", "Asia/Shanghai")
        self.weather_city_codes = {"北京": "101010100", "成都": "101270101"}
        self.weather_schedule_time = os.getenv("WEATHER_SCHEDULE_TIME", "01:00")

        self.milvus_host = os.getenv("MILVUS_HOST", "localhost")
        self.milvus_port = int(os.getenv("MILVUS_PORT", "19531"))
        self.tour_group_collection = os.getenv("TOUR_GROUP_COLLECTION", "tour_groups")

        self.embedding_url = os.getenv(
            "EMBEDDING_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings",
        )
        self.embedding_dim = int(os.getenv("EMBEDDING_DIM", "1024"))

        self.weather_a2a_url = os.getenv("WEATHER_A2A_URL", "http://127.0.0.1:5005")
        self.ticket_a2a_url = os.getenv("TICKET_A2A_URL", "http://127.0.0.1:5006")
        self.trip_a2a_url = os.getenv("TRIP_A2A_URL", "http://127.0.0.1:5007")
        self.weather_mcp_url = os.getenv("WEATHER_MCP_URL", "http://127.0.0.1:8002")
        self.ticket_mcp_url = os.getenv("TICKET_MCP_URL", "http://127.0.0.1:8001")
        self.trip_mcp_url = os.getenv("TRIP_MCP_URL", "http://127.0.0.1:8003")

        # 聚合数据火车订票查询（同步 12306 余票，非爬取官网）
        self.juhe_train_api_key = os.getenv("JUHE_TRAIN_API_KEY", "")

        # 携程跟团游：接入旁路 vac-product-recommend 脚本（需登录 Cookie）
        default_vac = os.path.normpath(
            os.path.join(project_root, "..", "vac-product-recommend-mcp-main")
        )
        self.vac_product_root = os.getenv("VAC_PRODUCT_ROOT", default_vac)
        self.ctrip_cookie_file = os.getenv("CTRIP_COOKIE_FILE", "")
        self.ctrip_cookie = os.getenv("CTRIP_COOKIE", "")

    def mysql_connect_kwargs(self):
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "charset": "utf8mb4",
            "collation": "utf8mb4_unicode_ci",
            "use_unicode": True,
            "use_pure": True,
        }


if __name__ == "__main__":
    cfg = Config()
    print(cfg.log_file)
    print(cfg.host, cfg.user, cfg.database, cfg.model_name)
