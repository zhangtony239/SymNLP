import subprocess
import sys
import time


def run_server():
    """运行server.py"""
    print("正在启动server.py...")
    server_process = subprocess.Popen([sys.executable, "server.py"])
    return server_process

def run_demo():
    """运行demo.py"""
    print("正在启动demo.py...")
    demo_process = subprocess.Popen([sys.executable, "demo.py"])
    return demo_process


if __name__ == "__main__":
    print("开始启动服务...")
    
    # 启动server进程
    server_proc = run_server()
    
    # 等待一段时间确保server已启动
    print("等待server启动...")
    time.sleep(3)
    
    # 启动demo进程
    demo_proc = run_demo()
    
    print("所有服务已启动！")
    print("Server PID:", server_proc.pid)
    print("Demo PID:", demo_proc.pid)
    
    try:
        # 等待两个进程结束
        server_proc.wait()
        demo_proc.wait()
    except KeyboardInterrupt:
        print("\n收到中断信号，正在关闭进程...")
        server_proc.terminate()
        demo_proc.terminate()
        
        # 等待进程结束或超时后强制杀死
        try:
            server_proc.wait(timeout=5)
            demo_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("进程未正常退出，尝试强制终止...")
            server_proc.kill()
            demo_proc.kill()