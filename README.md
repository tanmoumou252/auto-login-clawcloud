# ☁️ ClawCloud Auto-Login / 自动保活

此工作流旨在实现 **每天自动登录一次 ClawCloud (爪云)** 以保持账号活跃，没有webhook通知

修改[workflows](.github/workflows/clawcloud-login.yml)配置可以更改为更短或更长的时间

本脚本访问的域名为`https://ap-northeast-1.run.claw.cloud/`

为了确保自动化脚本顺利运行，**必须**满足以下条件：
1. ✅ **开启 2FA (双重验证)**：配合脚本中的 PyOTP 自动生成验证码，绕过异地登录风控。
2. ✅ **必须 Authenticator app 优先**：即使用2fa管理器获得一次性密码OTP的方式优先，强烈推荐[2fa浏览器插件](https://github.com/Authenticator-Extension/Authenticator)，不需要打开app，且能用密钥重现二维码
3. ❌ **可以不关闭 Passkey (通行密钥)**：但如果在workflows日志里有异常,可以移除Passkey 避免脚本无法处理生物识别弹窗。
---

## 🛠️ 配置步骤

### 第一步：Fork 本项目
点击页面右上角的 **Fork** 按钮，将此仓库复制到您的 GitHub 账号下。

### 第二步：开启 GitHub 2FA 并获取密钥
脚本需要通过 2FA 密钥自动计算验证码，因此不能只扫二维码，必须获取**文本密钥**。

1. 登录 GitHub，点击右上角头像 -> **Settings**。
2. 在左侧菜单选择 **Password and authentication**。
3. 找到 "Two-factor authentication" 区域，点击 **Enable 2FA**。
4. 选择 **Set up using an app**。
5. **⚠️ 关键步骤**：
   > 页面显示二维码时，**不要直接点击 Continue**。请点击二维码下方的蓝色小字 **"Setup Key"**（或 "enter this text code"）。
   >
   > 备注：该二维码使用非2fa客户端扫描也可以出现otp密钥 形如`otpauth://totp/GitHub:user?secret=NIHVNX********G&issuer=GitHub`
6. **复制显示的字符串密钥**（通常是 16 位字母数字组合）。
   * *注意：同时也请用手机验证器 App (如 Google Auth) 扫描二维码或输入密钥，以完成 GitHub 的验证流程。*
7. 再次强烈推荐[2fa浏览器插件](https://github.com/Authenticator-Extension/Authenticator)，不需要打开app，具备`自动填充`和域名匹配只显示当前站点的`智能过滤`

### 第三步：配置 GitHub Secrets
为了保护您的账号安全，请将敏感信息存储在仓库的 Secrets 中。

1. 进入您的 GitHub 仓库页面。
2. 依次点击导航栏的 **Settings** -> 左侧栏 **Secrets and variables** -> **Actions**。
3. 点击右上角的 **New repository secret** 按钮。
4. 依次添加以下 3 个 Secret：

| Secret 名称 | 填入内容 (Value) | 说明 |
| :--- | :--- | :--- |
| `GH_USERNAME` | **您的 GitHub 账号** | 通常是您的登录邮箱 |
| `GH_PASSWORD` | **您的 GitHub 密码** | 登录用的密码 |
| `GH_2FA_SECRET` | **2FA 密钥** | 第二步中复制的那串字符 (请去除空格) |

### 第四步：启用工作流权限 (⚠️ 重要)
由于是 Fork 的仓库，GitHub 默认可能会禁用 Actions 以防止滥用。

1. 点击仓库顶部的 **Actions** 选项卡。
2. 如果看到警告提示，请点击绿色的 **"I understand my workflows, go ahead and enable them"** 按钮。

### 第五步：手动测试运行
配置完成后，建议手动触发一次以确保一切正常。

1. 点击 **Actions** 选项卡。
2. 在左侧列表中选择 **ClawCloud Run Auto Login**。
3. 点击右侧的 **Run workflow** 下拉菜单 -> 点击绿色 **Run workflow** 按钮。
4. 等待运行完成，查看日志确保显示 `🎉 登录成功`。

---
**✅ 完成！之后脚本将每隔 1 天自动执行一次保活任务。**
