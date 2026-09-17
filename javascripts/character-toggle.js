
<script>
document.addEventListener('DOMContentLoaded', function() {
    var scriptType = localStorage.getItem('scriptType') || 'traditional';
    updateScriptDisplay(scriptType);
    
    function updateScriptDisplay(type) {
        document.querySelectorAll('.traditional-text').forEach(el => {
            el.style.display = type === 'traditional' ? 'block' : 'none';
        });
        document.querySelectorAll('.simplified-text').forEach(el => {
            el.style.display = type === 'simplified' ? 'block' : 'none';
        });
        localStorage.setItem('scriptType', type);
    }
    
    // Add toggle button to navigation
    var nav = document.querySelector('.md-header__inner');
    if (nav) {
        var toggleBtn = document.createElement('button');
        toggleBtn.className = 'md-header__button script-toggle';
        toggleBtn.innerHTML = scriptType === 'traditional' ? '繁體' : '简体';
        toggleBtn.onclick = function() {
            var newType = localStorage.getItem('scriptType') === 'traditional' ? 'simplified' : 'traditional';
            updateScriptDisplay(newType);
            this.innerHTML = newType === 'traditional' ? '繁體' : '简体';
        };
        nav.appendChild(toggleBtn);
    }
});
</script>
<style>
.script-toggle {
    margin-left: 1rem;
    padding: 0.5rem 1rem;
    border: 1px solid currentColor;
    border-radius: 4px;
    background: transparent;
    color: currentColor;
    cursor: pointer;
}
</style>
