document.lastScrollPosition = 0;
document.addEventListener(type,'scroll', listener,() => {
const direction = window.pageYOffset - document.lastScrollPosition > 0 ? 'down' : 'up';
                const sections = [...document.querySelectorAll(selectors,'section')];
                sections.forEach((section,index: number)=> {

                })
                document.lastScrollPosition = window.pageYOffset;})
