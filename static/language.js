(function () {

    const savedLanguage =
        localStorage.getItem("fileora_language") || "ar";

    function setLanguage(language) {

        localStorage.setItem(
            "fileora_language",
            language
        );

        document.documentElement.lang =
            language;

        document.documentElement.dir =
            language === "ar" ? "rtl" : "ltr";

        location.reload();
    }

    window.toggleLanguage = function () {

        const current =
            localStorage.getItem("fileora_language") || "ar";

        const next =
            current === "ar" ? "en" : "ar";

        setLanguage(next);
    };

    document.documentElement.lang =
        savedLanguage;

    document.documentElement.dir =
        savedLanguage === "ar" ? "rtl" : "ltr";

    const button =
        document.getElementById("languageBtn");

    if (button) {

        button.textContent =
            savedLanguage === "ar"
                ? "English"
                : "العربية";
    }

})();