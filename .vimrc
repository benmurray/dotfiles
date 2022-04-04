" bemurray's vimrc
" Ben Murray <ben@ruddydog.com>
" Copyright 2022 Ben Murray, all rights reserved.
" ==============
" Basic Settings
" ==============
call pathogen#infect()
set nocompatible	"Use vim, not vi
set relativenumber
set number " line I am on will be actual line number
set ruler
set encoding=utf-8
set cc=100
let NERDTreeIgnore = ['\.pyc$', '__pycache__']

call pathogen#helptags()

" set termguicolors
set t_Co=256
set mouse=a
syntax enable
let g:python_highlight_builtins=1
let g:python_highlight_doctests=1
let g:python_highlight_class_vars=1
let g:python_highlight_operators=1
let g:python_highlight_indent_errors=1
let g:python_highlight_space_errors=1
set background=dark
let g:solarized_termcolors=256
let g:solarized_termtrans=1
colorscheme monokai

" ===========
" Status Line
" ===========
set laststatus=2                        " Always how statusline
function! ChangeStatusLineColor()
    if &mod == 1
        " hi statusline ctermfg=16 ctermbg=228  " a faded yllow
        hi statusline ctermfg=16 ctermbg=3
    else
        hi statusline ctermfg=15 ctermbg=8
    endif
endfunction
au InsertLeave,InsertEnter,BufWritePost   * call ChangeStatusLineColor()

" flake8
" ==========
" let g:flake8_show_in_gutter=1  " show
" let g:flake8_show_in_file=0  " don't show (default)
" let g:flake8_show_in_file=1  " show

" ==========
" gitgutter
" ==========
set updatetime=125

" silence bell
set vb
" ==========
" Whitespace
" ==========
set nowrap
set tabstop=4
set shiftwidth=4
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
" Turn off swap files
set noswapfile
" set directory=~/.vim/_temp//      " where to put swap files.

" ==========
" File Types
" ==========
filetype plugin indent on         " filetype detection
autocmd FileType python setlocal expandtab shiftwidth=4 softtabstop=4
au BufNewFile,BufRead *.jinja set filetype=jinja
au BufNewFile,BufRead *.jinja2 set filetype=htmljinja
au BufNewFile,BufRead *.handlebars set filetype=handlebars

" ===============
" ctrlp Settings
" ===============
" First one contains vendor
"set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*/vendor/*,*/\.git/*
set wildignore+=*/tmp/*,*.so,*.swp,*.zip,*/\.git/*,*.pyc
let g:ctrlp_working_path_mode = 0
let g:ctrlp_max_height=10
let g:ctrlp_cache_dir = $HOME . '/.cache/ctrlp'

" ====
" Tags
" ====
set tags=./tags,tags;/
let g:tagbar_type_python = {
    \ 'kinds' : [
        \ 'i:imports:0:0',
        \ 'c:classes',
        \ 'f:functions',
        \ 'm:members',
        \ 'v:variables:0:0',
        \ '?:unknown',
    \ ],
\ }
" ========
" MAPPINGS
" ========
let mapleader = ","
" Bring up Todo's
nnoremap <leader>td :edit $HOME/.todos<cr>
	" Edit vimrc
nnoremap <leader>ev :vsplit $MYVIMRC<cr>
	" source vimrc
nnoremap <leader>sv :source $MYVIMRC<cr>
" bring up vim annoyances notes
nnoremap <leader>ea :edit $HOME/.vim_annoyances<cr>
	" call up NERDTree on current dir
"nnoremap <leader>, :NERDTree .<cr>
nnoremap <leader>,  :NERDTreeTabsToggle<cr>
nnoremap <leader>tb :TagbarToggle<cr>
nnoremap <leader>D :put =strftime(':date: %Y-%m-%d %H:%M:%S')<cr>

" Smash Escape
"  - removing for muscle memory reasons,
"  - this is not in every IDE emulator
inoremap jk <esc>
inoremap kj <esc>
vnoremap jk <esc>
vnoremap kj <esc>
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
iabbrev postion position
iabbrev continer container
	" Common Shortcuts
iabbrev @@ ben@ruddydog.com
iabbrev ssig --<cr>Ben Murray<cr>ben@ruddydog.com<cr>Ruddy Dog<cr>--<cr>
iabbrev ccopy Copyright 2022 Ben Murray, all rights reserved.
