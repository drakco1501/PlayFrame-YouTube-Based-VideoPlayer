
function previewProfileImage(input) {
    const preview = document.getElementById('previewImage');

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
        preview.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}
