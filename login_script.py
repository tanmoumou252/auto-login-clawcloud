# 文件名: login_script.py
import os
import time
from playwright.sync_api import sync_playwright

def run_login():
    # 1. 获取账号密码
    username = os.environ.get("GH_USERNAME")
    password = os.environ.get("GH_PASSWORD")
    if not username or not password:
        print("❌ 错误: 环境变量中未找到账号或密码。")
        return

    print("🚀 启动浏览器...")
    with sync_playwright() as p:
        # 启动浏览器 (headless=True 表示后台运行)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 2. 打开登录页
        target_url = "https://ap-northeast-1.run.claw.cloud/"
        print(f"🌐 正在访问: {target_url}")
        page.goto(target_url)
        page.wait_for_load_state("networkidle")

        # 截图看一眼初始状态
        # page.screenshot(path="debug_step1_start.png") 

        # 3. 点击 GitHub 登录按钮
        # 使用 get_by_role 确保只点击 "按钮"，避免点击到页面上的说明文字
        print("🔍 正在寻找 GitHub 按钮...")
        try:
            # 这种写法最稳：找一个 role 是 button，且名字里包含 GitHub 的元素
            login_button = page.get_by_role("button", name="GitHub", exact=False)
            
            if login_button.count() > 0:
                print("✅ 找到 GitHub 按钮，准备点击...")
                # 有些登录会弹窗，有些是跳转。使用 expect_popup 处理弹窗情况，同时兼顾跳转。
                with context.expect_page() as new_page_info:
                    # 如果是跳转，new_page_info 可能捕获不到，下面会有逻辑处理
                    # 如果是弹窗，这里会捕获到
                    try:
                        login_button.first.click(timeout=5000)
                    except Exception as e:
                        print(f"点击按钮时出现轻微异常 (通常不影响): {e}")
                
                # 稍微等待一下，判断是弹窗了还是本页跳转了
                page.wait_for_timeout(3000)
            else:
                print("❌ 未找到明确的 GitHub 按钮。")
        except Exception as e:
            # 如果没有弹窗，expect_page 可能会超时报错，这是正常的，说明是当前页跳转
            print("ℹ️ 点击后未检测到新窗口，假设是当前页跳转。")

        # 4. 处理 GitHub 登录逻辑
        # 我们需要判断当前是在哪个页面操作：是原来的 page 还是新的 popup_page？
        # 如果 pages 数量 > 1，说明弹窗了
        if len(context.pages) > 1:
            print("检测到弹出窗口，切换到新窗口进行登录...")
            login_page = context.pages[1] # 获取第二个窗口
        else:
            print("未检测到弹窗，继续在当前窗口操作...")
            login_page = page

        login_page.wait_for_load_state("networkidle")
        print(f"当前登录页标题: {login_page.title()}")
        
        # 填写 GitHub 账号密码
        if "github.com" in login_page.url:
            print("🔒 已到达 GitHub 验证页面，开始输入账号...")
            try:
                login_page.fill("#login_field", username)
                login_page.fill("#password", password)
                login_page.click("input[name='commit']") # 点击登录
                print("📤 已提交登录表单")
            except Exception as e:
                print(f"填写表单时遇到问题 (可能已自动登录): {e}")
            
            # 处理授权页面 (Authorize App)
            # 等待一会，看是否有授权按钮
            time.sleep(3)
            if "authorize" in login_page.url.lower():
                 print("检测到授权请求，尝试点击 Authorize...")
                 try:
                     # 尝试点击绿色的授权按钮
                     login_page.click("button:has-text('Authorize')", timeout=4000)
                 except:
                     pass
        else:
            print(f"⚠️ 当前 URL 不是 GitHub ({login_page.url})，跳过填写步骤。")

        # 5. 等待最终跳转
        print("⏳ 等待跳转回控制台...")
        # 给它足够的时间完成重定向
        page.wait_for_timeout(10000) 
        
        # 重新获取主页面的 URL
        final_url = page.url
        print(f"最终页面 URL: {final_url}")
        
        # 截图保存结果
        page.screenshot(path="login_result.png")
        print("📸 已保存截图 login_result.png")

        # 6. 精确判断成功
        # 成功的标志：URL 不包含 'signin' 且 (包含 'console' 或 'dashboard' 或页面上有特定元素)
        # 根据您提供的成功图片，成功后应该能看到 "App Launchpad"
        is_success = False
        
        if "signin" not in final_url and "login" not in final_url:
            # 进一步验证页面内容
            if page.get_by_text("App Launchpad").count() > 0 or page.get_by_text("Devbox").count() > 0:
                is_success = True
            # 如果 URL 是类似 console.claw.cloud 也算成功
            elif "private-team" in final_url or "console" in final_url:
                is_success = True

        if is_success:
            print("🎉🎉🎉 登录成功！检测到控制台元素。")
        else:
            print("😭😭😭 登录失败。停留在登录页或被拦截。")
            # 强制抛出异常，让 GitHub Actions 显示红色的 X
            exit(1)

        browser.close()

if __name__ == "__main__":
    run_login()
