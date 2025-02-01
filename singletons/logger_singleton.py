import logging

class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.logger = logging.getLogger("app_logger")
            cls._instance.logger.setLevel(logging.DEBUG)

            # Add console handler
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            cls._instance.logger.addHandler(handler)

        return cls._instance

    def get_logger(self):
        return self.logger
