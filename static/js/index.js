document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("form[id^='edit-form-']").forEach((form) => {
    const reviewId = form.id.split("-").pop();

    // Lấy modal container
    const modalContainer = form.closest("[id^='review-modal-']");
    if (!modalContainer) return;

    // Nút Save bên trong modal footer
    const saveButton = modalContainer.querySelector("button[data-save-button]");
    if (!saveButton) return;

    // Lấy modal body chứa form
    const modalBody = modalContainer.querySelector(".modal-body");
    if (!modalBody) return;

    saveButton.addEventListener("click", function () {
      // Tạo loading overlay nếu chưa có
      let loadingOverlay = modalBody.querySelector(".modal-loading-overlay");
      if (!loadingOverlay) {
        loadingOverlay = document.createElement("div");
        loadingOverlay.classList.add("modal-loading-overlay");

        // Spinner
        const spinner = document.createElement("div");
        spinner.classList.add("spinner");
        loadingOverlay.appendChild(spinner);

        // Đảm bảo modalBody position relative để overlay phủ đúng
        const style = window.getComputedStyle(modalBody);
        if (style.position === "static") {
          modalBody.style.position = "relative";
        }

        modalBody.appendChild(loadingOverlay);
      }

      // Hiện overlay
      loadingOverlay.classList.add("show");

      const formData = new FormData(form);

      fetch(`/api/reviews/${reviewId}`, {
        method: "POST",
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            alert("Update successful!");
            location.reload();
          } else {
            alert("Update failed.");
          }
        })
        .catch(() => alert("Error during update."))
        .finally(() => {
          // Ẩn overlay
          loadingOverlay.classList.remove("show");
        });
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Gán event click cho tất cả nút Delete trong modal confirm
  document.querySelectorAll("[data-delete-button]").forEach((button) => {
    button.addEventListener("click", function () {
      const reviewIndex = button.getAttribute("data-delete-button");
      const deleteModal = document.getElementById(
        `delete-modal-${reviewIndex}`
      );
      const reviewId = parseInt(reviewIndex); // theo logic bạn đang dùng review_index == review_id

      // Gọi API DELETE
      fetch(`/api/reviews/${reviewId}`, {
        method: "DELETE",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            alert("Delete successful!");
            // Đóng modall
            const flowbiteModal = window.Modal.getInstance(deleteModal);
            if (flowbiteModal) flowbiteModal.hide();
            // Reload trang để cập nhật bảng
            location.reload();
          } else {
            alert("Delete failed: " + (data.error || "Unknown error"));
          }
        })
        .catch((err) => {
          alert("Delete error: " + err.message);
        });
    });
  });
});
function handleClick(element) {
  const value = element.dataset.value || "";
  alert(`Value: ${value}`);
}
