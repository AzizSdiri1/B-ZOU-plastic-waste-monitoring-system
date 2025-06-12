async function fetchImage() {
    const image = document.getElementById("display-image");
    const error = document.getElementById("error");

    try {
        const response = await fetch("/image/fetch-image");
        if (response.ok) {
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            image.src = imageUrl;
            image.classList.remove("hidden");
            error.textContent = "";
            // Revoke the object URL after the image loads to free memory
            image.onload = () => URL.revokeObjectURL(imageUrl);
        } else {
            error.textContent = "Failed to capture image";
        }
    } catch (err) {
        error.textContent = "Failed to fetch image";
    }
}