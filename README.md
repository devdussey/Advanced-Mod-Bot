# Discord Advanced Moderation Bot

An advanced moderation bot with:
- Slash commands for moderation (ban, kick, mute, warn)
- Jail system (dynamic jail role, with original roles restored)
- Auto roles on member join
- Neat embed logs
- SQLite database persistence

---

## 🚀 Features
- `/ban @user reason`
- `/kick @user reason`
- `/mute @user minutes reason`
- `/warn @user reason` (saved to DB)
- `/warnings @user` (check warnings)
- `/setjailrole @role` → set jail role
- `/jail @user reason` → jail user
- `/unjail @user` → release user
- `/setautorole @role` → add autorole
- `/clearautoroles` → clear autoroles
- `/setlogchannel #channel` → set log channel

---

## 🛠 Setup (Replit)
1. Create a new Python Repl  
2. Drag & drop all files from the `.zip` into the Repl  
3. Open **Secrets Manager** in Replit (lock icon on left)  
   - Add `DISCORD_TOKEN` → your bot token from Discord Developer Portal  
   - Add `GUILD_ID` → your server’s ID (right click server > Copy ID)  
4. Replit will auto-install dependencies from `requirements.txt`  
5. Hit **Run** — your bot should go online ✅

---

## 🧑‍💻 Notes
- SQLite database (`database.sqlite3`) persists in your Repl  
- Use `/setjailrole`, `/setautorole`, `/setlogchannel` after first launch to configure  
- Requires Discord’s **Message Content Intent** and **Server Members Intent** enabled in Developer Portal
