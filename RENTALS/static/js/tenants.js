document.addEventListener('DOMContentLoaded', function() {
    const selectAllBtn = document.getElementById('selectAllTenants');
    const deleteBtn = document.getElementById('deleteSelectedTenantsBtn');

    // Helper to get CSRF token from the hidden input or cookie
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    }

    // 1. Handle "Select All"
    if (selectAllBtn) {
        selectAllBtn.addEventListener('change', function() {
            // Re-query checkboxes in case the DOM updated
            const tenantCheckboxes = document.querySelectorAll('.tenant-checkbox');
            tenantCheckboxes.forEach(cb => {
                cb.checked = this.checked;
            });
            toggleDeleteButton();
        });
    }

    // 2. Individual Checkbox Change (using Event Delegation)
    document.addEventListener('change', function(e) {
        if (e.target.classList.contains('tenant-checkbox')) {
            toggleDeleteButton();
        }
    });

    // 3. Show/Hide Delete Button
    function toggleDeleteButton() {
        const checkedCount = document.querySelectorAll('.tenant-checkbox:checked').length;
        if (deleteBtn) {
            deleteBtn.style.display = checkedCount > 0 ? 'inline-block' : 'none';
        }
    }

    // 4. Delete Action
    if (deleteBtn) {
        deleteBtn.addEventListener('click', function() {
            const selectedIds = Array.from(document.querySelectorAll('.tenant-checkbox:checked'))
                .map(cb => cb.value);

            if (selectedIds.length === 0) return;

            if (confirm(`Are you sure you want to delete ${selectedIds.length} tenant(s)? This will also vacate their units.`)) {
                const formData = new FormData();
                selectedIds.forEach(id => formData.append('tenant_ids[]', id));

                // If this is in a separate JS file, replace '{% url ... %}' with '/tenants/delete/'
                const targetUrl = '{% url "tenants:delete_tenants" %}'; 

                fetch(targetUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert(data.message || 'Error deleting tenants');
                    }
                })
                .catch(err => {
                    console.error('Error:', err);
                    alert('Server error. Check if the URL is correct.');
                });
            }
        });
    }
});