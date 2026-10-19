document.addEventListener("DOMContentLoaded", function () {
    const workerSelect = document.getElementById("id_assigned_workers");

    if (
        workerSelect &&
        workerSelect.tagName === "SELECT" &&
        workerSelect.multiple &&
        typeof Choices !== "undefined"
    ) {
        new Choices(workerSelect, {
            removeItemButton: true,
            searchEnabled: true,
            shouldSort: false,
            itemSelectText: "",
            placeholder: true,
            placeholderValue: "Search and select workers...",
            searchPlaceholderValue: "Type a worker's name..."
        });
    }
});