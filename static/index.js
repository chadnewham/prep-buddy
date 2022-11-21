
let checkboxes = document.querySelectorAll('input.custom-checkbox')


checkboxes.forEach(check=>{
    check.addEventListener('click', (e)=>{
        
        check.closest('tr').classList.toggle('positive')
    })
})