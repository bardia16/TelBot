 #!/bin/bash

# Configuration
PID_FILE="bot.pid"
LOG_FILE="bot.log"
PYTHON_SCRIPT="main.py"

# Colors for status messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper function to check if bot is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0 # true, bot is running
        fi
    fi
    return 1 # false, bot is not running
}

# Start the bot
start() {
    echo "Starting Telegram Link Collector Bot..."
    
    if is_running; then
        echo -e "${YELLOW}Bot is already running with PID $(cat $PID_FILE)${NC}"
        exit 1
    fi
    
    # Start the bot with nohup
    nohup python3 -u "$PYTHON_SCRIPT" > "$LOG_FILE" 2>&1 & echo $! > "$PID_FILE"
    
    # Wait a moment to check if process is still running
    sleep 2
    if is_running; then
        echo -e "${GREEN}Bot started successfully with PID $(cat $PID_FILE)${NC}"
    else
        echo -e "${RED}Failed to start bot. Check $LOG_FILE for details${NC}"
        rm -f "$PID_FILE"
        exit 1
    fi
}

# Stop the bot
stop() {
    echo "Stopping Telegram Link Collector Bot..."
    
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            kill "$pid"
            sleep 2
            if ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${YELLOW}Bot didn't stop gracefully, forcing...${NC}"
                kill -9 "$pid" 2>/dev/null
            fi
            rm -f "$PID_FILE"
            echo -e "${GREEN}Bot stopped successfully${NC}"
        else
            echo -e "${YELLOW}Bot not running but PID file exists. Cleaning up...${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${RED}Bot not running (no PID file)${NC}"
        exit 1
    fi
}

# Check bot status
status() {
    if is_running; then
        pid=$(cat "$PID_FILE")
        echo -e "${GREEN}Bot is running with PID $pid${NC}"
        echo "Recent logs:"
        tail -n 5 "$LOG_FILE"
    else
        echo -e "${RED}Bot is not running${NC}"
        [ -f "$PID_FILE" ] && rm -f "$PID_FILE"
    fi
}

# Command line interface
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0