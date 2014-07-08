" bemur's vimrc
" Ben Murray <bemur@ruddydog.com>
" Copyright 2012 Ben Murray, all rights reserved. 


" ==============
" Basic Settings
" ==============
call pathogen#infect()
set nocompatible	"Use vim, not vi
set relativenumber
set ruler
syntax on
set encoding=utf-8
set background=dark

" ==========
" Whitespace
" ==========
set nowrap
set tabstop=2
set shiftwidth=2
set expandtab
set list		" Show invisible characters
set backspace=indent,eol,start

" ==========
" List chars
" ==========
set listchars=""                  " Reset the listchars
set listchars=tab:\ \             " a tab should display as "  ", trailing whitespace as "."
set listchars+=trail:.            " show trailing spaces as dots
set listchars+=extends:>          " The character to show in the last column when wrap is
                                  " off and the line continues beyond the right of the screen
set listchars+=precedes:<         " The character to show in the last column when wrap is
                                  " off and the line continues beyond the right of the screen

" =========
" Searching
" =========
set hlsearch    " highlight matches
set incsearch   " incremental searching
set ignorecase  " searches are case insensitive...
set smartcase   " ... unless they contain at least one capital letter

" ======
" Backup
" ======
set backupdir=~/.vim/_backup//    " where to put backup files.
set directory=~/.vim/_temp//      " where to put swap files.

" ==========
" File Types
" ==========
filetype plugin indent on         " filetype detection
autocmd FileType python setlocal expandtab shiftwidth=4 softtabstop=4
au BufNewFile,BufRead *.jinja set filetype=jinja
au BufNewFile,BufRead *.jinja2 set filetype=htmljinja
au BufNewFile,BufRead *.handlebars set filetype=handlebars

" ========
" MAPPINGS
" ========
inoremap {      {}<Left>
inoremap {<CR>  {<CR>}<Esc>O
inoremap {{     {
inoremap {}     {}
inoremap <expr> )  strpart(getline('.'), col('.')-1, 1) == ")" ? "\<Right>" : ")"

let mapleader = ","
	" Edit vimrc
nnoremap <leader>ev :vsplit $MYVIMRC<cr>
	" source vimrc
nnoremap <leader>sv :source $MYVIMRC<cr>
	" call up NERDTree on current dir
nnoremap <leader>, :NERDTree .<cr>
nnoremap <leader>tb :TagbarToggle<cr>
inoremap jk <esc>
"inoremap <esc> <nop>
vnoremap jk <esc>
"vnoremap <esc> <nop>
noremap <leader>w <c-w><c-w>
" Toggle Toolbar "
nnoremap <leader>got :if &go=~#'T'<Bar>set go-=T<Bar>else<Bar>set go+=T<Bar>endif<CR>
" Toggle Menu "
nnoremap <leader>gom :if &go=~#'M'<Bar>set go-=m<Bar>else<Bar>set go+=m<Bar>endif<CR>
" Toggle Right-hand scroll"
nnoremap <leader>gor :if &go=~#'r'<Bar>set go-=r<Bar>else<Bar>set go+=r<Bar>endif<CR>
" Toggle Bottom scroll"
nnoremap <leader>gob :if &go=~#'b'<Bar>set go-=b<Bar>else<Bar>set go+=b<Bar>endif<CR>

" =============
" Abbreviations
" =============
	" Common mispellings
iabbrev adn and
iabbrev waht what
iabbrev tehn then
	" Common Shortcuts
iabbrev @@ ben.murray@arnold.af.mil
iabbrev ssig --<cr>Ben Murray<cr>ben.murray@arnold.af.mil<cr>Aerospace Testing Alliance<cr>931-454-5788<cr>--<cr>
iabbrev ccopy Copyright 2011 Ben Murray, all rights reserved.

" ===========
" GUI RUNNING
" ===========
if has('gui_running')
" set guifont=Consolas:h12:cANSI " On windows boxes
  colorscheme railscasts
" set guifont=Ubuntu\ Mono\ 12
	set guioptions-=T   " Get rid of toolbar "
"	set guioptions-=m   " Get rid of menu    "
"	set go-=r	    " Get rid of scrollbars "
endif
