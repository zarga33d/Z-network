import pexpect
import time
import sys
import os
import random
from time import sleep
import threading
import argparse

# إعداد معالج المعاملات
def parse_arguments():
    parser = argparse.ArgumentParser(description='ZaNet - أداة التحكم الآلي في EvilLimiter')
    parser.add_argument('-L', '--language', choices=['arabic', 'english'], default='english',
                        help='اختيار لغة الواجهة (arabic/english)')
    return parser.parse_args()

# تحديد لغة الواجهة
def setup_language(language):
    if language == 'arabic':
        return {
            'initializing': 'جاري تهيئة النظام...',
            'analyzing_network': 'تحليل الشبكة...',
            'scanning_ports': 'فحص المنافذ المفتوحة...',
            'discovering_devices': 'اكتشاف الأجهزة المتصلة...',
            'checking_protocols': 'جاري فحص بروتوكولات الشبكة...',
            'analyzing_traffic': 'تحليل حركة المرور...',
            'preparing_tools': 'جاري تحضير أدوات المراقبة...',
            'zarga': 'zarga',
            'initializing_controls': 'تهيئة أدوات التحكم بالشبكة...',
            'setting_up_monitors': 'جاري إعداد برامج المراقبة...',
            'checking_vulnerabilities': 'فحص نقاط الضعف...',
            'preparing_hack_tools': 'تجهيز أدوات الاختراق...',
            'setting_up_interface': 'جاري إعداد واجهة التحكم...',
            'analyzing_security': 'تحليل متطلبات الأمان...',
            'preparing_evillimiter': 'جاري تحضير EvilLimiter...',
            
            'root_required': 'يجب تشغيل هذا السكربت بصلاحيات الجذر (sudo)',
            'starting_evillimiter': 'جاري تشغيل EvilLimiter...',
            'evillimiter_started': 'تم تشغيل EvilLimiter بنجاح',
            'performing_scan': 'جاري إجراء عملية المسح رقم {}...',
            'scan_completed': 'اكتملت عملية المسح رقم {}',
            'blocking_devices': 'جاري حظر جميع الأجهزة...',
            'blocking_completed': 'تم حظر جميع الأجهزة بنجاح',
            'operations_completed': 'تم تنفيذ جميع العمليات المطلوبة. البرنامج مستمر في التشغيل.',
            'press_ctrl_c': 'اضغط Ctrl+C للخروج من البرنامج',
            'exiting_program': 'جاري إنهاء البرنامج...',
            'exit_success': 'تم إنهاء البرنامج بنجاح',
            'error_occurred': 'حدث خطأ أثناء تشغيل EvilLimiter: {}',
            'user_interrupted': 'تم إنهاء البرنامج بواسطة المستخدم',
            'error': 'حدث خطأ: {}',
            'animation_cycles': 'اكتملت {} دورة من الانيميشنات',
            'tool_description': 'أداة التحكم الآلي في EvilLimiter - تنفذ 3 عمليات مسح ثم تحظر جميع الأجهزة'
        }
    else:  # English
        return {
            'initializing': 'Initializing system...',
            'analyzing_network': 'Analyzing network...',
            'scanning_ports': 'Scanning open ports...',
            'discovering_devices': 'Discovering connected devices...',
            'checking_protocols': 'Checking network protocols...',
            'analyzing_traffic': 'Analyzing traffic...',
            'preparing_tools': 'Preparing monitoring tools...',
            'zarga': 'zarga',
            'initializing_controls': 'Initializing network control tools...',
            'setting_up_monitors': 'Setting up monitoring programs...',
            'checking_vulnerabilities': 'Checking vulnerabilities...',
            'preparing_hack_tools': 'Preparing penetration tools...',
            'setting_up_interface': 'Setting up control interface...',
            'analyzing_security': 'Analyzing security requirements...',
            'preparing_evillimiter': 'Preparing EvilLimiter...',
            
            'root_required': 'This script must be run with root privileges (sudo)',
            'starting_evillimiter': 'Starting EvilLimiter...',
            'evillimiter_started': 'EvilLimiter started successfully',
            'performing_scan': 'Performing scan #{} ...',
            'scan_completed': 'Scan #{} completed',
            'blocking_devices': 'Blocking all devices...',
            'blocking_completed': 'All devices blocked successfully',
            'operations_completed': 'All operations completed. Program is still running.',
            'press_ctrl_c': 'Press Ctrl+C to exit the program',
            'exiting_program': 'Exiting program...',
            'exit_success': 'Program terminated successfully',
            'error_occurred': 'Error occurred while running EvilLimiter: {}',
            'user_interrupted': 'Program terminated by user',
            'error': 'Error: {}',
            'animation_cycles': 'Completed {} animation cycles',
            'tool_description': 'EvilLimiter Automation Tool - Performs 3 scans then blocks all devices'
        }

# قائمة الانيميشنات - 15 انيميشن مختلف
animations = [
    # 1. انيميشن دائرة دوارة
    ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    
    # 2. انيميشن شريط تقدم
    ["[=    ]", "[==   ]", "[===  ]", "[==== ]", "[=====]", "[ ====]", "[  ===]", "[   ==]", "[    =]", "[     ]"],
    
    # 3. انيميشن نبض
    ["●∙∙∙∙", "∙●∙∙∙", "∙∙●∙∙", "∙∙∙●∙", "∙∙∙∙●", "∙∙∙●∙", "∙∙●∙∙", "∙●∙∙∙"],
    
    # 4. انيميشن قلب نابض
    ["❤️  ", " ❤️ ", "  ❤️", " ❤️ "],
    
    # 5. انيميشن تحميل بسيط
    [".  ", ".. ", "...", " ..", "  .", "   "],
    
    # 6. انيميشن كتل متحركة
    ["▉▉▉▉▉", "▊▉▉▉▉", "▋▊▉▉▉", "▌▋▊▉▉", "▍▌▋▊▉", "▎▍▌▋▊", "▏▎▍▌▋", "▎▍▌▋▊", "▍▌▋▊▉", "▌▋▊▉▉", "▋▊▉▉▉", "▊▉▉▉▉"],
    
    # 7. انيميشن قرصنة
    ["[░░░░░░░░░░]", "[█░░░░░░░░░]", "[██░░░░░░░░]", "[███░░░░░░░]", "[████░░░░░░]", 
     "[█████░░░░░]", "[██████░░░░]", "[███████░░░]", "[████████░░]", "[█████████░]", "[██████████]"],
    
    # 8. انيميشن مصباح
    ["💡 ", " 💡", "💡 "],
    
    # 9. انيميشن سهم دوار
    ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"],
    
    # 10. انيميشن مكعبات متحركة
    ["▁▂▃▄▅▆▇█", "█▁▂▃▄▅▆▇", "▇█▁▂▃▄▅▆", "▆▇█▁▂▃▄▅", "▅▆▇█▁▂▃▄", "▄▅▆▇█▁▂▃", "▃▄▅▆▇█▁▂", "▂▃▄▅▆▇█▁"],
    
    # 11. انيميشن نجمة متحركة
    ["✶", "✸", "✹", "✺", "✹", "✷"],
    
    # 12. انيميشن قطار
    ["🚂💨  ", " 🚂💨 ", "  🚂💨", "   🚂💨"],
    
    # 13. انيميشن هاكر
    ["[ʜᴀᴄᴋɪɴɢ.]", "[ʜᴀᴄᴋɪɴɢ..]", "[ʜᴀᴄᴋɪɴɢ...]", "[ʜᴀᴄᴋɪɴɢ....]"],
    
    # 14. انيميشن شبكة
    ["⚡️ ", " ⚡️", "  ⚡️", " ⚡️"],
    
    # 15. انيميشن دائرة نقاط
    ["◜ ", " ◝", " ◞", "◟ "]
]

# متغير للتحكم في استمرار الانيميشن
animation_running = True

def display_animation(strings):
    """وظيفة لعرض الانيميشنات بالترتيب"""
    global animation_running
    iteration = 0
    
    # قائمة الرسائل
    messages = [
        strings['initializing'],
        strings['analyzing_network'],
        strings['scanning_ports'],
        strings['discovering_devices'],
        strings['checking_protocols'],
        strings['analyzing_traffic'],
        strings['preparing_tools'],
        strings['zarga'],  # هنا تم إضافة اسم zarga كما طلبت
        strings['initializing_controls'],
        strings['setting_up_monitors'],
        strings['checking_vulnerabilities'],
        strings['preparing_hack_tools'],
        strings['setting_up_interface'],
        strings['analyzing_security'],
        strings['preparing_evillimiter']
    ]
    
    while animation_running:
        # تكرار الدورة عند الانتهاء من جميع الانيميشنات
        for anim_idx, animation in enumerate(animations):
            # عرض الرسالة المناسبة مع الانيميشن
            message = messages[anim_idx % len(messages)]
            
            # عرض الانيميشن الحالي
            for frame in animation:
                if not animation_running:
                    return
                    
                # مسح السطر السابق وعرض الإطار الحالي
                sys.stdout.write(f"\r{frame} {message}" + " " * 20)
                sys.stdout.flush()
                sleep(0.1)
            
        iteration += 1
        # عرض رسالة بعد كل دورة كاملة
        if iteration % 2 == 0:
            sys.stdout.write("\r\033[K")  # مسح السطر
            sys.stdout.flush()
            print(f"\n[+] {strings['animation_cycles'].format(iteration // 2)}")
            sleep(0.5)

def run_evillimiter(strings):
    """الوظيفة الرئيسية لتشغيل EvilLimiter"""
    global animation_running
    
    # التحقق من تشغيل البرنامج كمستخدم جذر (root)
    if os.geteuid() != 0:
        print(strings['root_required'])
        sys.exit(1)
    
    # عرض شعار البداية بألوان مميزة
    display_banner(strings)
    
    # بدء سلسلة الانيميشنات في خيط منفصل
    animation_thread = threading.Thread(target=display_animation, args=(strings,))
    animation_thread.daemon = True
    animation_thread.start()
    
    # انتظار قليلاً لعرض الانيميشنات
    sleep(8)
    
    # إيقاف الانيميشن قبل بدء EvilLimiter
    animation_running = False
    animation_thread.join(timeout=1)
    
    # مسح السطر الأخير
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()
    
    print(f"\n[+] {strings['starting_evillimiter']}\n")
    
    try:
        # تشغيل EvilLimiter
        child = pexpect.spawn('sudo evillimiter')
        
        # انتظار ظهور واجهة EvilLimiter
        child.expect('>>> ')
        print(f"[+] {strings['evillimiter_started']}")
        
        # إجراء 3 عمليات مسح
        for scan_count in range(1, 4):
            print(f"[*] {strings['performing_scan'].format(scan_count)}")
            
            # إرسال أمر المسح
            child.sendline('scan')
            
            # إعادة تشغيل الانيميشن أثناء المسح
            animation_running = True
            animation_thread = threading.Thread(target=display_animation, args=(strings,))
            animation_thread.daemon = True
            animation_thread.start()
            
            # انتظار اكتمال المسح
            time.sleep(15)
            
            # إيقاف الانيميشن
            animation_running = False
            animation_thread.join(timeout=1)
            
            # مسح السطر الأخير
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()
            
            # انتظار عودة الواجهة
            child.expect('>>> ')
            print(f"[+] {strings['scan_completed'].format(scan_count)}")
        
        # حظر جميع الأجهزة المكتشفة
        print(f"\n[*] {strings['blocking_devices']}")
        child.sendline('block all')
        child.expect('>>> ')
        print(f"[+] {strings['blocking_completed']}")
        
        # الاستمرار في التشغيل حتى يقرر المستخدم الإنهاء
        print(f"\n[i] {strings['operations_completed']}")
        print(f"[i] {strings['press_ctrl_c']}")
        
        try:
            # إبقاء البرنامج مفتوحاً
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            # إرسال أمر الخروج عند الضغط على Ctrl+C
            print(f"\n[*] {strings['exiting_program']}")
            child.sendline('quit')
            print(f"[+] {strings['exit_success']}")
    
    except Exception as e:
        print(f"\n[!] {strings['error_occurred'].format(e)}")
        sys.exit(1)

def display_banner(strings):
    """عرض شعار البداية بألوان مميزة"""
    banner = """
\033[91m███████╗ █████╗ ███╗   ██╗███████╗████████╗
\033[93m   ███╔╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝
\033[92m  ███╔╝ ███████║██╔██╗ ██║█████╗     ██║   
\033[96m ███╔╝  ██╔══██║██║╚██╗██║██╔══╝     ██║   
\033[94m███████╗██║  ██║██║ ╚████║███████╗   ██║   
\033[95m╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   
\033[97m                                 v1.0
\033[0m"""
    print(banner)
    print("\033[93m" + "=" * 80 + "\033[0m")
    print(f"\033[96m[i] {strings['tool_description']}\033[0m")
    print("\033[93m" + "=" * 80 + "\033[0m\n")

def main():
    # معالجة المعاملات
    args = parse_arguments()
    
    # تحديد لغة الواجهة
    strings = setup_language(args.language)
    
    try:
        run_evillimiter(strings)
    except KeyboardInterrupt:
        print(f"\n\033[93m[!] {strings['user_interrupted']}\033[0m")
        global animation_running
        animation_running = False
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[91m[!] {strings['error'].format(e)}\033[0m")
        animation_running = False
        sys.exit(1)

if __name__ == "__main__":
    main()
