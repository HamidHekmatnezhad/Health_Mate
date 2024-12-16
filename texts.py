
help_en = """
# User Guide for Vital Information Registration System

## Enrollment

To register in the system:

1. **Select Enrollment Option**:
   - Select the **Enrollment** option.

2. **Enter Personal Information**:
   - Choose a unique **ID**.
   - Enter your first name and last name.
   - Select your gender (Male/Female/None).
   - Enter your year of birth.

3. **Upload Photo**:
   - Take a clear photo of your face. Please ensure the photo is clear and unfiltered.
   - After taking the photo, submit it.
   - Once the photo is approved, your registration will be complete.

## Health Mate

To register vital information:

1. **Identification Method**:
   - You have two options for identification:
     - **Enter ID**: Input your ID.
     - **Facial Recognition**: Use the device's camera for facial recognition.

2. **Access Information Section**:
   - After selecting one of the methods, enter the relevant section.
   - Your vital information will be retrieved from the microcontroller and entered into the system.

## Show Record

To view registered vital information:

1. **Identification Method**:
   - Choose one of the two methods:
     - **Enter ID**: Input your ID.
     - **Facial Recognition**: Use the device's camera for facial recognition.

2. **Retrieve Information**:
   - After identification, your vital information will be displayed.

## Settings

- **This section is under development...**
  - New features will be added to this section soon.

## Edit Infos

To edit personal information:

1. **Access Edit Section**:
   - Go to the **Edit Infos** section.

2. **Edit Information**:
   - Modify any personal information that needs to be changed.
   - After completing the edits, save the changes.

---
"""

help_fr_html = """
<div dir="rtl">

<h1>راهنمای کاربر برای سیستم ثبت اطلاعات حیاتی</h1>

<h2>ثبت نام</h2>

<p>برای ثبت نام در سیستم:</p>

<ol>
    <li><strong>انتخاب گزینه ثبت نام:</strong>
        <ul>
            <li>گزینه <strong>ثبت نام</strong> را انتخاب کنید.</li>
        </ul>
    </li>
    <li><strong>وارد کردن اطلاعات شخصی:</strong>
        <ul>
            <li>یک <strong>ID</strong> منحصر به فرد انتخاب کنید.</li>
            <li>نام و نام خانوادگی خود را وارد کنید.</li>
            <li>جنسیت خود را انتخاب کنید (مرد/زن/هیچ‌کدام).</li>
            <li>سال تولد خود را وارد کنید.</li>
        </ul>
    </li>
    <li><strong>بارگذاری عکس:</strong>
        <ul>
            <li>یک عکس واضح از چهره خود بگیرید. لطفاً اطمینان حاصل کنید که عکس واضح و بدون فیلتر باشد.</li>
            <li>پس از گرفتن عکس، آن را ارسال کنید.</li>
            <li>پس از تایید عکس، ثبت نام شما تکمیل خواهد شد.</li>
        </ul>
    </li>
</ol>

<h2>سلامت یار</h2>

<p>برای ثبت اطلاعات حیاتی:</p>

<ol>
    <li><strong>روش شناسایی:</strong>
        <ul>
            <li>شما دو گزینه برای شناسایی دارید:
                <ul>
                    <li><strong>وارد کردن ID:</strong> ID خود را وارد کنید.</li>
                    <li><strong>تشخیص چهره:</strong> از دوربین دستگاه برای تشخیص چهره استفاده کنید.</li>
                </ul>
            </li>
        </ul>
    </li>
    <li><strong>دسترسی به بخش اطلاعات:</strong>
        <ul>
            <li>پس از انتخاب یکی از روش‌ها، به بخش مربوطه وارد شوید.</li>
            <li>اطلاعات حیاتی شما از میکروکنترلر گرفته شده و به سیستم وارد خواهد شد.</li>
        </ul>
    </li>
</ol>

<h2>نمایش اطلاعات</h2>

<p>برای مشاهده اطلاعات حیاتی ثبت شده:</p>

<ol>
    <li><strong>روش شناسایی:</strong>
        <ul>
            <li>یکی از دو روش زیر را انتخاب کنید:
                <ul>
                    <li><strong>وارد کردن ID:</strong> ID خود را وارد کنید.</li>
                    <li><strong>تشخیص چهره:</strong> از دوربین دستگاه برای تشخیص چهره استفاده کنید.</li>
                </ul>
            </li>
        </ul>
    </li>
    <li><strong>دریافت اطلاعات:</strong>
        <ul>
            <li>پس از شناسایی، اطلاعات حیاتی شما نمایش داده خواهد شد.</li>
        </ul>
    </li>
</ol>

<h2>تنظیمات</h2>

<p><strong>این بخش در حال توسعه است...</strong></p>
<p>به زودی امکانات جدیدی به این بخش اضافه خواهد شد.</p>

<h2>ویرایش اطلاعات فردی</h2>

<p>برای ویرایش اطلاعات شخصی:</p>

<ol>
    <li><strong>دسترسی به بخش ویرایش:</strong>
        <ul>
            <li>به بخش <strong>ویرایش اطلاعات</strong> بروید.</li>
        </ul>
    </li>
    <li><strong>ویرایش اطلاعات:</strong>
        <ul>
            <li>هر اطلاعات شخصی که نیاز به تغییر دارد را ویرایش کنید.</li>
            <li>پس از اتمام ویرایش، تغییرات را ذخیره کنید.</li>
        </ul>
    </li>
</ol>

<hr>

</div>
"""

footer_html = """
<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: white;
text-align: center;
}
.bb {
    font-weight: bold; 
    
</style>
<div class="footer">
<p>Developed with <span class="bb">Hamid Hekmatnezhad</span> and <span class="bb">Dr. Amard Afzalian</span>. © 2024 All rights reserved.</p>
</div>
"""

developers = """ 
### Dr. Amard Afzalian
- **Field:** Assistant Professor of Electrical and Electronic Engineering, Islamic Azad University, Ramsar Branch
- **Role:** Hardware Programming, Electronics Design, Microcontroller Programming
- **Email:** afzalian.iau@gmail.com

---
---

### Hamid Hekmatnezhad
- **Field:** Computer Engineering, Islamic Azad University, Ramsar Branch
- **Role:** Software Develope, Database Design, Facial Recognition System Design, Microcontroller Programming
- **Email:** hhekmatnezhad@gmail.com
"""