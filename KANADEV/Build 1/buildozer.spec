with open("buildozer.spec", "w") as f:
    f.write("""
[app]
title = KANADEV
package.name = kanadev
package.domain = org.kana.dev
source.dir = .
source.include_exts = py,png,kv,atlas,otf
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
[buildozer]
log_level = 2
warn_on_root = 0
android.sdk = 34
android.ndk = 25b
    """)
    
