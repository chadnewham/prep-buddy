

document.addEventListener('keypress', (e)=>{
    if(e.key == 'Enter'){
        e.preventDefault()
        let inputList = document.querySelectorAll('input.custom-input-focus')
        let currentIndex = Array.from(inputList).indexOf(document.activeElement)
        console.log(inputList.length)
        if(currentIndex < inputList.length -1){
            inputList.item(currentIndex+1).focus()
        }else{
            inputList.item(0).focus()
        }
    }
})