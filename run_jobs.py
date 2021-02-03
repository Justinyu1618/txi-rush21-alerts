from server import create_app
from datetime import datetime, timedelta

if __name__ == '__main__':
    app = create_app()
    from server.sms.alert import run_alerts
    run_alerts()
