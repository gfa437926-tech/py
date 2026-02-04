import flet as ft
from supabase import create_client, Client

# --- بيانات الربط (أدخل بياناتك هنا) ---
URL = "https://vktcvkwqszehgmhqjrkb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrdGN2a3dxc3plaGdtaHFqcmtiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIxNzE3NTEsImV4cCI6MjA3Nzc0Nzc1MX0.KTX1c8BAJpy1Jp3-IDXFRqb4Jo7SLabiwICBtn_mR5o"

# تهيئة الاتصال بقاعدة البيانات
supabase: Client = create_client(URL, KEY)

def main(page: ft.Page):
    # إعدادات الصفحة
    page.title = "Supabase Cloud App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # المكونات (UI)
    title_text = ft.Text("إرسال بيانات للسحابة", size=28, weight="bold", color="blue")
    msg_input = ft.TextField(
        label="اكتب رسالتك هنا",
        hint_text="مثلاً: السلام عليكم",
        border_radius=15,
        width=350,
        multiline=True
    )
    status_text = ft.Text("", size=16)
    loading_ring = ft.ProgressRing(visible=False, width=20, height=20)

    # وظيفة الإرسال
    def send_data(e):
        if not msg_input.value:
            status_text.value = "⚠️ من فضلك اكتب رسالة أولاً"
            status_text.color = "orange"
            page.update()
            return

        # إظهار مؤشر التحميل
        loading_ring.visible = True
        status_text.value = "جاري الإرسال..."
        status_text.color = "blue"
        page.update()

        try:
            # إدخال البيانات في جدول اسمه messages (تأكد أن الجدول موجود في Supabase)
            response = supabase.table("messages").insert({"content": msg_input.value}).execute()
            
            status_text.value = "✅ تم الإرسال بنجاح!"
            status_text.color = "green"
            msg_input.value = "" # تفريغ الحقل بعد النجاح
        except Exception as ex:
            status_text.value = f"❌ خطأ: {str(ex)}"
            status_text.color = "red"
        
        loading_ring.visible = False
        page.update()

    # زر الإرسال
    submit_btn = ft.ElevatedButton(
        text="إرسال إلى Supabase",
        icon=ft.icons.SEND_ROUNDED,
        on_click=send_data,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20
        )
    )

    # إضافة العناصر للصفحة
    page.add(
        ft.Icon(ft.icons.CLOUD_SYNC_ROUNDED, size=80, color="blue"),
        title_text,
        ft.Divider(height=20, color="transparent"),
        msg_input,
        ft.Row([loading_ring, status_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=10, color="transparent"),
        submit_btn
    )

# تشغيل التطبيق
ft.app(target=main)