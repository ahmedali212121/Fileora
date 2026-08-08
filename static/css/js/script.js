const uploadBox = document.getElementById("uploadBox");
const input = document.getElementById("pdf_file");
const fileName = document.getElementById("file-name");
const form = document.getElementById("uploadForm");
const loading = document.getElementById("loading");
const button = document.getElementById("convertBtn");
const langBtn = document.getElementById("langBtn");

let currentLang = "ar";


/* =========================
   اختيار الملف
========================= */

function showFile(file) {

    if (!file) {
        return;
    }

    if (file.type !== "application/pdf") {

        fileName.textContent =
            currentLang === "ar"
                ? "❌ يرجى اختيار ملف PDF فقط"
                : "❌ Please choose a PDF file only";

        input.value = "";

        return;
    }

    fileName.textContent = "✅ " + file.name;

    const dataTransfer = new DataTransfer();

    dataTransfer.items.add(file);

    input.files = dataTransfer.files;
}


input.addEventListener("change", function () {

    if (this.files.length > 0) {
        showFile(this.files[0]);
    }

});


/* =========================
   السحب والإفلات
========================= */

uploadBox.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadBox.classList.add("drag-over");

});


uploadBox.addEventListener("dragleave", function () {

    uploadBox.classList.remove("drag-over");

});


uploadBox.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadBox.classList.remove("drag-over");

    const file = event.dataTransfer.files[0];

    showFile(file);

});


/* =========================
   التحويل
========================= */

form.addEventListener("submit", function (event) {

    if (!input.files.length) {

        event.preventDefault();

        fileName.textContent =
            currentLang === "ar"
                ? "❌ اختر ملف PDF أولًا"
                : "❌ Please choose a PDF file first";

        return;
    }

    loading.style.display = "block";

    button.disabled = true;

    button.textContent =
        currentLang === "ar"
            ? "جاري التحويل..."
            : "Converting...";

});


/* =========================
   تغيير اللغة
========================= */

if (langBtn) {

    langBtn.addEventListener("click", function () {

        const title = document.querySelector(".converter-header h1");
        const description = document.querySelector(".converter-header p");
        const uploadTitle = document.querySelector(".upload-box h2");
        const uploadText = document.querySelector(".upload-box p");
        const backButton = document.querySelector(".back-button");
        const navHome = document.querySelector(".nav-links a");
        const navTool = document.querySelectorAll(".nav-links a")[1];

        if (currentLang === "ar") {

            document.documentElement.lang = "en";
            document.documentElement.dir = "ltr";

            title.textContent = "Convert PDF to Word";

            description.textContent =
                "Convert your PDF file to Word quickly and easily.";

            uploadTitle.textContent =
                "Drag & Drop your PDF here";

            uploadText.textContent =
                "Or click here to choose a file from your computer";

            if (fileName.textContent === "لم يتم اختيار ملف") {
                fileName.textContent = "No file selected";
            }

            button.textContent =
                "🚀 Convert to Word";

            backButton.textContent =
                "← Back to Home";

            navHome.textContent =
                "Home";

            navTool.textContent =
                "PDF to Word";

            langBtn.textContent =
                "العربية";

            currentLang = "en";

        } else {

            document.documentElement.lang = "ar";
            document.documentElement.dir = "rtl";

            title.textContent =
                "تحويل PDF إلى Word";

            description.textContent =
                "حوّل ملف PDF إلى مستند Word بسهولة وسرعة.";

            uploadTitle.textContent =
                "اسحب ملف PDF هنا";

            uploadText.textContent =
                "أو اضغط هنا لاختيار ملف من جهازك";

            if (fileName.textContent === "No file selected") {
                fileName.textContent = "لم يتم اختيار ملف";
            }

            button.textContent =
                "🚀 تحويل إلى Word";

            backButton.textContent =
                "← العودة إلى الصفحة الرئيسية";

            navHome.textContent =
                "الرئيسية";

            navTool.textContent =
                "PDF إلى Word";

            langBtn.textContent =
                "English";

            currentLang = "ar";

        }

    });

}