# Web Scraping service for an E-library

## Features:

- simple scrolling interface of recomended books ready for user upon entering.
  
- Every panel consists of a way to link to the website.
  
- search technology producing 20 results at a time to reduce information overload.
  
- Selecting a book from recommendation panel introduces info like:
  
  - Book Name
    
  - Author
    
  - Publisher
    
  - ISBN (International Standard Book Number, originally 9 numeric characters)
    
  - ISBN 10 (10 numerica characters)
    
  - ISBN 13 (13 numberic characters)
    
  - File type (what format the book is available in)
    
  - No. of pages
    
  - Small description (if available on the site)
    
- While selecting a book from the search results open a small frame consisting some useful info from above and two buttons.
  
  - A button to share the book details as a note
    
  - A button to download the book (Due to the site being a non-profit organization, this project will open the link to the book details page in a browser) from where the user will be able to ownload th book.
    

## Cons:

- Time Complexity.
  
- This project works on line-by-line sequential execution, GUI will not be available between processes.
  
- No threads are applied in this version.
  
- Many features are not added yet (This is an exoskeleton of the idea).
  
- Algorithm redundantly uses variables, and methods.
  
- GUI is quite naive.
  
- Static sizing of the Interface sometimes pose a problem when the frame is resized.
  

##### Requirements:

| Package | Usage |
| --- | --- |
| Wxpython | For GUI Development |
| urllib | For making requests to the site |
| BS4 | For Scraping data from the recieved webpage |
| io  | For recieveing Multimedia data |
| pyscreenshot | For creating the sharing card |
| win32gui | Aiding pyscreenshot for accurate capturing |
| webbrowser | For opening book links in the browser |

---

> ## Future releases may contain:
> 
> - [ ] A redesigned UI
>   
> - [ ] More tooltips
>   
> - [ ] More shortcuts
>   
> - [ ] modular approach to the workflow.
>   
> - [ ] Threads
>   
> - [ ] Link to other websites where the material can be found
>   
> - [ ] Article search
>   
> - [ ] Download history
>   
> - [ ] Reader
>   
> - [ ] profile management
>   
> - [ ] More Deprecation warning!!
>   

```python
print("Education is our passport to the future, for tommorrow belongs to
        people who prepare for it today\n --Malcolm X")
```
