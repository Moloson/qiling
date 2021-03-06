#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
# Built on top of Unicorn emulator (www.unicorn-engine.org) 
import sys
import os
import string

from qiling.const import *
from qiling.exception import *

from qiling.loader.loader import QlLoader

PT_LOAD = 1
PT_DYNAMIC = 2
PT_INTERP = 3

ET_REL = 1
ET_EXEC = 2
ET_DYN = 3

AT_NULL = 0
AT_IGNORE = 1
AT_EXECFD = 2
AT_PHDR = 3
AT_PHENT = 4
AT_PHNUM = 5
AT_PAGESZ = 6
AT_BASE = 7
AT_FLAGS = 8
AT_ENTRY = 9
AT_NOTELF = 10
AT_UID = 11
AT_EUID = 12
AT_GID = 13
AT_EGID = 14
AT_PLATFORM = 15
AT_HWCAP = 16
AT_CLKTCK = 17
AT_SECURE = 23
AT_BASE_PLATFORM = 24
AT_RANDOM = 25
AT_HWCAP2 = 26
AT_EXECFN = 31

FILE_DES = []
#MMAP_START = 0

class ELFParse(QlLoader):
    def __init__(self, path, ql):
        self.path = os.path.abspath(path)
        self.ql = ql

        with open(path, "rb") as f:
            elfdata = f.read()

        self.elfdata = elfdata.ljust(52, b'\x00')        

        self.ident = self.getident()

        if self.ident[ : 4] != b'\x7fELF':
            raise QlErrorELFFormat("[!] ERROR: NOT a ELF")

        self.elfhead = self.parse_header()

    def getident(self):
        return self.elfdata[0 : 19]

    def getelfdata(self, offest, size):
        return self.elfdata[offest : offest + size]

    def parse_header32(self):
        # typedef struct elf32_hdr{
        # unsigned char	e_ident[EI_NIDENT];
        # Elf32_Half	e_type;
        # Elf32_Half	e_machine;
        # Elf32_Word	e_version;
        # Elf32_Addr	e_entry;  /* Entry point */
        # Elf32_Off	e_phoff;
        # Elf32_Off	e_shoff;
        # Elf32_Word	e_flags;
        # Elf32_Half	e_ehsize;
        # Elf32_Half	e_phentsize;
        # Elf32_Half	e_phnum;
        # Elf32_Half	e_shentsize;
        # Elf32_Half	e_shnum;
        # Elf32_Half	e_shstrndx;
        # } Elf32_Ehdr;

        # /* 32-bit ELF base types. */
        # typedef uint32_t Elf32_Addr;
        # typedef uint16_t Elf32_Half;
        # typedef uint32_t Elf32_Off;
        # typedef int32_t  Elf32_Sword;
        # typedef uint32_t Elf32_Word;

        data = self.elfdata
        index = 0
        head = {}
        head['e_ident']         = data[index : index + 16];                     index += 16
        head['e_type']          = self.ql.unpack16(data[index : index + 2]);    index += 2
        head['e_machine']       = self.ql.unpack16(data[index : index + 2]);    index += 2
        head['e_version']       = self.ql.unpack32(data[index : index + 4]);    index += 4
        head['e_entry']         = self.ql.unpack32(data[index : index + 4]);    index += 4
        head['e_phoff']         = self.ql.unpack32(data[index : index + 4]);    index += 4
        head['e_shoff']         = self.ql.unpack32(data[index : index + 4]);    index += 4
        head['e_flags']         = self.ql.unpack32(data[index : index + 4]);    index += 4
        head['e_ehsize']        = self.ql.unpack16(data[index : index + 2]);    index += 2
        head['e_phentsize']     = self.ql.unpack16(data[index : index + 2]);    index += 2
        head['e_phnum']         = self.ql.unpack16(data[index : index + 2]);    index += 2
        head['e_shentsize']     = self.ql.unpack16(data[index : index + 2]);    index += 2
        head['e_shnum']         = self.ql.unpack16(data[index : index + 2]);    index += 2
        head['e_shstrndx']      = self.ql.unpack16(data[index : index + 2]);    index += 2
        return head

    def parse_header64(self):
        # typedef struct elf64_hdr {
        # unsigned char	e_ident[16];		/* ELF "magic number" */
        # Elf64_Half e_type;
        # Elf64_Half e_machine;
        # Elf64_Word e_version;
        # Elf64_Addr e_entry;		/* Entry point virtual address */
        # Elf64_Off e_phoff;		/* Program header table file offset */
        # Elf64_Off e_shoff;		/* Section header table file offset */
        # Elf64_Word e_flags;
        # Elf64_Half e_ehsize;
        # Elf64_Half e_phentsize;
        # Elf64_Half e_phnum;
        # Elf64_Half e_shentsize;
        # Elf64_Half e_shnum;
        # Elf64_Half e_shstrndx;
        # } Elf64_Ehdr;

        # /* 64-bit ELF base types. */
        # typedef uint64_t Elf64_Addr;
        # typedef uint16_t Elf64_Half;
        # typedef int16_t	 Elf64_SHalf;
        # typedef uint64_t Elf64_Off;
        # typedef int32_t	 Elf64_Sword;
        # typedef uint32_t Elf64_Word;
        # typedef uint64_t Elf64_Xword;
        # typedef int64_t  Elf64_Sxword;

        data = self.elfdata
        index = 0
        head = {}
        head['e_ident']         = data[index : index + 16];                 index += 16
        head['e_type']          = self.ql.unpack16(data[index : index + 2]);     index += 2
        head['e_machine']       = self.ql.unpack16(data[index : index + 2]);     index += 2
        head['e_version']       = self.ql.unpack32(data[index : index + 4]);     index += 4
        head['e_entry']         = self.ql.unpack64(data[index : index + 8]);     index += 8
        head['e_phoff']         = self.ql.unpack64(data[index : index + 8]);     index += 8
        head['e_shoff']         = self.ql.unpack64(data[index : index + 8]);     index += 8
        head['e_flags']         = self.ql.unpack32(data[index : index + 4]);     index += 4
        head['e_ehsize']        = self.ql.unpack16(data[index : index + 2]);     index += 2
        head['e_phentsize']     = self.ql.unpack16(data[index : index + 2]);     index += 2
        head['e_phnum']         = self.ql.unpack16(data[index : index + 2]);     index += 2
        head['e_shentsize']     = self.ql.unpack16(data[index : index + 2]);     index += 2
        head['e_shnum']         = self.ql.unpack16(data[index : index + 2]);     index += 2
        head['e_shstrndx']      = self.ql.unpack16(data[index : index + 2]);     index += 2
        return head
    
    def parse_header(self):
        if self.ql.archbit == 64:
            return self.parse_header64()
        elif self.ql.archbit == 32:
            return self.parse_header32()

    def parse_section_header32(self):
        # typedef struct elf32_shdr {
        # Elf32_Word	sh_name;
        # Elf32_Word	sh_type;
        # Elf32_Word	sh_flags;
        # Elf32_Addr	sh_addr;
        # Elf32_Off	sh_offset;
        # Elf32_Word	sh_size;
        # Elf32_Word	sh_link;
        # Elf32_Word	sh_info;
        # Elf32_Word	sh_addralign;
        # Elf32_Word	sh_entsize;
        # } Elf32_Shdr;

        # /* 32-bit ELF base types. */
        # typedef uint32_t Elf32_Addr;
        # typedef uint16_t Elf32_Half;
        # typedef uint32_t Elf32_Off;
        # typedef int32_t  Elf32_Sword;
        # typedef uint32_t Elf32_Word;

        Ssize = self.elfhead['e_shentsize']
        Snum = self.elfhead['e_shnum']
        Sdata = self.elfdata[self.elfhead['e_shoff'] : self.elfhead['e_shoff'] + Snum * Ssize]
        
        for i in range(Snum):
            S = {}
            S['sh_name']        = self.ql.unpack32(Sdata[i * Ssize : i * Ssize + 4])
            S['sh_type']        = self.ql.unpack32(Sdata[i * Ssize + 4 : i * Ssize + 8])
            S['sh_flags']       = self.ql.unpack32(Sdata[i * Ssize + 8 : i * Ssize + 12])
            S['sh_addr']        = self.ql.unpack32(Sdata[i * Ssize + 12 : i * Ssize + 16])
            S['sh_offset']      = self.ql.unpack32(Sdata[i * Ssize + 16 : i * Ssize + 20])
            S['sh_size']        = self.ql.unpack32(Sdata[i * Ssize + 20 : i * Ssize + 24])
            S['sh_link']        = self.ql.unpack32(Sdata[i * Ssize + 24 : i * Ssize + 28])
            S['sh_info']        = self.ql.unpack32(Sdata[i * Ssize + 28 : i * Ssize + 32])
            S['sh_addralign']   = self.ql.unpack32(Sdata[i * Ssize + 32 : i * Ssize + 36])
            S['sh_entsize']     = self.ql.unpack32(Sdata[i * Ssize + 36 : i * Ssize + 40])
            S['data']           = self.elfdata[S['sh_offset'] : S['sh_offset'] + S['sh_size']]
            yield S
        return

    def parse_section_header64(self):
        # typedef struct elf64_shdr {
        # Elf64_Word sh_name;		/* Section name, index in string tbl */
        # Elf64_Word sh_type;		/* Type of section */
        # Elf64_Xword sh_flags;		/* Miscellaneous section attributes */
        # Elf64_Addr sh_addr;		/* Section virtual addr at execution */
        # Elf64_Off sh_offset;		/* Section file offset */
        # Elf64_Xword sh_size;		/* Size of section in bytes */
        # Elf64_Word sh_link;		/* Index of another section */
        # Elf64_Word sh_info;		/* Additional section information */
        # Elf64_Xword sh_addralign;	/* Section alignment */
        # Elf64_Xword sh_entsize;	/* Entry size if section holds table */
        # } Elf64_Shdr;

        # /* 64-bit ELF base types. */
        # typedef uint64_t Elf64_Addr;
        # typedef uint16_t Elf64_Half;
        # typedef int16_t	 Elf64_SHalf;
        # typedef uint64_t Elf64_Off;
        # typedef int32_t	 Elf64_Sword;
        # typedef uint32_t Elf64_Word;
        # typedef uint64_t Elf64_Xword;
        # typedef int64_t  Elf64_Sxword;

        Ssize = self.elfhead['e_shentsize']
        Snum = self.elfhead['e_shnum']
        Sdata = self.elfdata[self.elfhead['e_shoff'] : self.elfhead['e_shoff'] + Snum * Ssize]

        for i in range(Snum):
            S = {}
            S['sh_name']        = self.ql.unpack32(Sdata[i * Ssize : i * Ssize + 4])
            S['sh_type']        = self.ql.unpack32(Sdata[i * Ssize + 4 : i * Ssize + 8])
            S['sh_flags']       = self.ql.unpack64(Sdata[i * Ssize + 8 : i * Ssize + 16])
            S['sh_addr']        = self.ql.unpack64(Sdata[i * Ssize + 16 : i * Ssize + 24])
            S['sh_offset']      = self.ql.unpack64(Sdata[i * Ssize + 24 : i * Ssize + 32])
            S['sh_size']        = self.ql.unpack64(Sdata[i * Ssize + 32 : i * Ssize + 40])
            S['sh_link']        = self.ql.unpack32(Sdata[i * Ssize + 40 : i * Ssize + 44])
            S['sh_info']        = self.ql.unpack32(Sdata[i * Ssize + 44 : i * Ssize + 48])
            S['sh_addralign']   = self.ql.unpack64(Sdata[i * Ssize + 48 : i * Ssize + 56])
            S['sh_entsize']     = self.ql.unpack64(Sdata[i * Ssize + 56 : i * Ssize + 64])
            S['data']           = self.elfdata[S['sh_offset'] : S['sh_offset'] + S['sh_size']]
            yield S
        return

    def parse_section_header(self):
        if self.ql.archbit == 64:
            return self.parse_section_header64()
        elif self.ql.archbit == 32:
            return self.parse_section_header32()

    def parse_program_header32(self):
        # typedef struct elf32_phdr{
        # Elf32_Word	p_type;
        # Elf32_Off	p_offset;
        # Elf32_Addr	p_vaddr;
        # Elf32_Addr	p_paddr;
        # Elf32_Word	p_filesz;
        # Elf32_Word	p_memsz;
        # Elf32_Word	p_flags;
        # Elf32_Word	p_align;
        # } Elf32_Phdr;

        # /* 32-bit ELF base types. */
        # typedef uint32_t Elf32_Addr;
        # typedef uint16_t Elf32_Half;
        # typedef uint32_t Elf32_Off;
        # typedef int32_t  Elf32_Sword;
        # typedef uint32_t Elf32_Word;

        Psize = int(self.elfhead['e_phentsize'])
        Pnum = int(self.elfhead['e_phnum'])
        Pdata = self.elfdata[self.elfhead['e_phoff'] : self.elfhead['e_phoff'] + Pnum * Psize]

        for i in range(Pnum):
            P = {}
            P['p_type']     = self.ql.unpack32(Pdata[i * Psize : i * Psize + 4 ])
            P['p_offset']   = self.ql.unpack32(Pdata[i * Psize + 4 : i * Psize + 8 ])
            P['p_vaddr']    = self.ql.unpack32(Pdata[i * Psize + 8 : i * Psize + 12 ])
            P['p_paddr']    = self.ql.unpack32(Pdata[i * Psize + 12 : i * Psize + 16 ])
            P['p_filesz']   = self.ql.unpack32(Pdata[i * Psize + 16 : i * Psize + 20 ])
            P['p_memsz']    = self.ql.unpack32(Pdata[i * Psize + 20 : i * Psize + 24 ])
            P['p_flags']    = self.ql.unpack32(Pdata[i * Psize + 24 : i * Psize + 28 ])
            P['p_align']    = self.ql.unpack32(Pdata[i * Psize + 28 : i * Psize + 32])
            yield P
        return

    def parse_program_header64(self):
        # typedef struct elf64_phdr {
        # Elf64_Word p_type;
        # Elf64_Word p_flags;
        # Elf64_Off p_offset;		/* Segment file offset */
        # Elf64_Addr p_vaddr;		/* Segment virtual address */
        # Elf64_Addr p_paddr;		/* Segment physical address */
        # Elf64_Xword p_filesz;		/* Segment size in file */
        # Elf64_Xword p_memsz;		/* Segment size in memory */
        # Elf64_Xword p_align;		/* Segment alignment, file & memory */
        # } Elf64_Phdr;

        # /* 64-bit ELF base types. */
        # typedef uint64_t Elf64_Addr;
        # typedef uint16_t Elf64_Half;
        # typedef int16_t	 Elf64_SHalf;
        # typedef uint64_t Elf64_Off;
        # typedef int32_t	 Elf64_Sword;
        # typedef uint32_t Elf64_Word;
        # typedef uint64_t Elf64_Xword;
        # typedef int64_t  Elf64_Sxword;

        Psize = self.elfhead['e_phentsize']
        Pnum = self.elfhead['e_phnum']
        Pdata = self.elfdata[self.elfhead['e_phoff'] : self.elfhead['e_phoff'] + Pnum * Psize]

        for i in range(Pnum):
            P = {}
            P['p_type']     = self.ql.unpack32(Pdata[i * Psize : i * Psize + 4 ])
            P['p_flags']    = self.ql.unpack32(Pdata[i * Psize + 4 : i * Psize + 8 ])
            P['p_offset']   = self.ql.unpack64(Pdata[i * Psize + 8 : i * Psize + 16 ])
            P['p_vaddr']    = self.ql.unpack64(Pdata[i * Psize + 16 : i * Psize + 24 ])
            P['p_paddr']    = self.ql.unpack64(Pdata[i * Psize + 24 : i * Psize + 32 ])
            P['p_filesz']   = self.ql.unpack64(Pdata[i * Psize + 32 : i * Psize + 40 ])
            P['p_memsz']    = self.ql.unpack64(Pdata[i * Psize + 40 : i * Psize + 48 ])
            P['p_align']    = self.ql.unpack64(Pdata[i * Psize + 48 : i * Psize + 56])
            yield P
        return

    def parse_program_header(self):
        if self.ql.archbit == 64:
            return self.parse_program_header64()
        elif self.ql.archbit == 32:
            return self.parse_program_header32()

class QlLoaderELF(ELFParse, QlLoader):
    def __init__(self, ql):
        super()
        self.ql = ql
        self.path = self.ql.path
        if not self.ql.shellcoder:
            ELFParse.__init__(self, self.path, self.ql)
        self.interp_base = 0
        self.mmap_start = 0
        # specially for syscall_execve()
        #self.load()
        if not self.ql.shellcoder:
            self.load_with_ld(self.ql, self.ql.stack_address + self.ql.stack_size, argv = self.ql.argv, env = self.ql.env)
            self.ql.stack_address  = (int(self.new_stack))

    def pack(self, data):
        if self.ql.archbit == 64:
            return self.ql.pack64(data)
        elif self.ql.archbit == 32:
            return self.ql.pack32(data)
        else:
            return self.ql.pack32(data)

    def copy_str(self, uc, addr, l):
        l_addr = []
        s_addr = addr
        for i in l:
            s_addr = s_addr - len(i) - 1
            # if isinstance(i, bytes):
            #     # self.ql.nprint(type(b'\x00'))
            # self.ql.nprint(type(i))
            # self.ql.nprint(i)
            # self.ql.nprint(type(i.encode()))
            # self.ql.nprint(type(addr))
            #     uc.mem_write(s_addr, i + b'\x00')
            # else:
            
            self.ql.mem.write(s_addr, i.encode() + b'\x00')
            l_addr.append(s_addr)
        return l_addr, s_addr

    def alignment(self, val):
        if self.ql.archbit == 64:
            return (val // 8) * 8
        elif self.ql.archbit == 32:
            return (val // 4) * 4

    def NEW_AUX_ENT(self, key, val):
        if self.ql.archbit == 32:
            return self.ql.pack32(int(key)) + self.ql.pack32(int(val))
        elif self.ql.archbit == 64:
            return self.ql.pack64(int(key)) + self.ql.pack64(int(val))

    def NullStr(self, s):
        return s[ : s.find(b'\x00')]

    def load_with_ld(self, ql, stack_addr, loadbase = -1, argv = [], env = {}):

        if loadbase <= 0:
            if self.ql.archbit == 64:
                loadbase = 0x555555554000
            elif self.ql.archtype== QL_MIPS32:
                loadbase = 0x0000004fef000
            else:
                loadbase = 0x56555000

        elfhead = super().parse_header()

        # Determine the range of memory space opened up
        mem_start = -1
        mem_end = -1
        interp_path = ''
        for i in super().parse_program_header():
            if i['p_type'] == PT_LOAD:
                if mem_start > i['p_vaddr'] or mem_start == -1:
                    mem_start = i['p_vaddr']
                if mem_end < i['p_vaddr'] + i['p_memsz'] or mem_end == -1:
                    mem_end = i['p_vaddr'] + i['p_memsz']
            if i['p_type'] == PT_INTERP:
                interp_path = self.NullStr(super().getelfdata(i['p_offset'], i['p_filesz']))

        mem_start = int(mem_start // 0x1000) * 0x1000
        mem_end = int(mem_end // 0x1000 + 1) * 0x1000

        if elfhead['e_type'] == ET_EXEC:
            loadbase = 0
        elif elfhead['e_type'] != ET_DYN:
            self.ql.nprint("[+] Some error in head e_type: %u!" %elfhead['e_type'])
            return -1

        self.ql.mem.map(loadbase + mem_start, mem_end - mem_start)
        self.ql.mem.add_mapinfo(loadbase + mem_start, loadbase + mem_end, 'r-x', self.path)

        for i in super().parse_program_header():
            if i['p_type'] == PT_LOAD:
                self.ql.mem.write(loadbase + i['p_vaddr'], super().getelfdata(i['p_offset'], i['p_filesz']))
                self.ql.dprint(D_INFO,
                          "[+] load 0x%x - 0x%x" % (loadbase + i['p_vaddr'], loadbase + i['p_vaddr'] + i['p_filesz']))

        entry_point = elfhead['e_entry'] + loadbase

        self.ql.dprint(D_INFO, "[+] mem_start: 0x%x mem_end: 0x%x" % (mem_start, mem_end))

        self.brk_address = mem_end + loadbase

        # Load interpreter if there is an interpreter

        if interp_path != '':
            interp_path = str(interp_path, 'utf-8', errors="ignore")
           
            interp = ELFParse(ql.rootfs + interp_path, ql)
            interphead = interp.parse_header()
            self.ql.dprint(D_INFO, "[+] interp is : %s" % (ql.rootfs + interp_path))

            interp_mem_size = -1
            for i in interp.parse_program_header():
                if i['p_type'] == PT_LOAD:
                    if interp_mem_size < i['p_vaddr'] + i['p_memsz'] or interp_mem_size == -1:
                        interp_mem_size = i['p_vaddr'] + i['p_memsz']
            interp_mem_size = (interp_mem_size // 0x1000 + 1) * 0x1000
            self.ql.dprint(D_INFO, "[+] interp_mem_size is : 0x%x" % int(interp_mem_size))

            if self.ql.interp_base == 0:
                if self.ql.archbit == 64:
                    self.interp_base = 0x7ffff7dd5000
                elif self.ql.archbit == 32 and self.ql.archtype!= QL_MIPS32:
                    self.interp_base = 0xfb7d3000
                elif self.ql.archtype== QL_MIPS32:
                    self.interp_base = 0x00000047ba000
                else:
                    self.interp_base = 0xff7d5000
            else:
                self.interp_base = self.ql.interp_base

            self.ql.dprint(D_INFO, "[+] interp_base is : 0x%x" % (self.interp_base))
            self.ql.mem.map(self.interp_base, int(interp_mem_size))
            self.ql.mem.add_mapinfo(self.interp_base, self.interp_base + int(interp_mem_size), 'r-x',os.path.abspath(interp_path))

            for i in interp.parse_program_header():
                if i['p_type'] == PT_LOAD:
                    self.ql.mem.write(self.interp_base + i['p_vaddr'], interp.getelfdata(i['p_offset'], i['p_filesz']))
            entry_point = interphead['e_entry'] + self.interp_base

        # Set MMAP addr
        if self.ql.mmap_start == 0:
            if self.ql.archbit == 64:
                self.mmap_start = 0x7ffff7dd6000 - 0x40000000
            elif self.ql.archtype== QL_MIPS32:
                self.mmap_start = 0x7ffef000 - 0x4000000
                if self.ql.archendian == QL_ENDIAN_EB:
                    self.mmap_start  = 0x778bf000 - 0x400000
            else:
                self.mmap_start = 0xf7fd6000 - 0x400000
        else:
            self.mmap_start = self.ql.mmap_start

        self.ql.dprint(D_INFO, "[+] mmap_start is : 0x%x" % (self.mmap_start))

        # Set elf table
        elf_table = b''
        new_stack = stack_addr

        # Set argc
        #if self.ql.archbit == 32:
        #    elf_table += self.ql.pack32(len(argv))
        #else:
        elf_table += self.pack(len(argv))

        # Set argv
        if len(argv) != 0:
            argv_addr, new_stack = self.copy_str(ql.uc, stack_addr, argv)

            if self.ql.archbit == 32:
                elf_table += b''.join([ql.pack32(_) for _ in argv_addr])
            elif self.ql.archbit == 64:
                elf_table += b''.join([ql.pack64(_) for _ in argv_addr])

        if self.ql.archbit == 32:
            elf_table += self.ql.pack32(0)
        elif self.ql.archbit == 64:
            elf_table += self.ql.pack64(0)

        # Set env
        if len(env) != 0:
            env_addr, new_stack = self.copy_str(ql.uc, new_stack, [key + '=' + value for key, value in env.items()])
            if self.ql.archbit == 32:
                elf_table += b''.join([ql.pack32(_) for _ in env_addr])
            elif self.ql.archbit == 64:
                elf_table += b''.join([ql.pack64(_) for _ in env_addr])

        if self.ql.archbit == 32:
            elf_table += self.ql.pack32(0)
        elif self.ql.archbit == 64:
            elf_table += self.ql.pack64(0)

        new_stack = self.alignment(new_stack)

        randstr = 'a' * 0x10
        cpustr = 'i686'
        (addr, new_stack) = self.copy_str(ql.uc, new_stack, [randstr, cpustr])
        new_stack = self.alignment(new_stack)

        # Set AUX

        # self.ql.mem.write(int(new_stack) - 4, self.ql.pack32(0x11111111))
        # new_stack = new_stack - 4
        # rand_addr = new_stack - 4

        self.elf_phdr     = (loadbase + elfhead['e_phoff'])
        self.elf_phent    = (elfhead['e_phentsize'])
        self.elf_phnum    = (elfhead['e_phnum'])
        self.elf_pagesz   = 0x1000
        if self.ql.archendian == QL_ENDIAN_EB:
            self.elf_pagesz   = 0x0010
        self.elf_guid     = 1000
        self.elf_flags    = 0
        self.elf_entry    = (loadbase + elfhead['e_entry'])
        self.randstraddr  = addr[0]
        self.cpustraddr   = addr[1]
        if self.ql.archbit == 64:
            self.elf_hwcap = 0x078bfbfd
        elif self.ql.archbit == 32:
            self.elf_hwcap = 0x1fb8d7
            if self.ql.archendian == QL_ENDIAN_EB:
                self.elf_hwcap = 0xd7b81f

        elf_table += self.NEW_AUX_ENT(AT_PHDR, self.elf_phdr + mem_start)
        elf_table += self.NEW_AUX_ENT(AT_PHENT, self.elf_phent)
        elf_table += self.NEW_AUX_ENT(AT_PHNUM, self.elf_phnum)
        elf_table += self.NEW_AUX_ENT(AT_PAGESZ, self.elf_pagesz)
        elf_table += self.NEW_AUX_ENT(AT_BASE, self.interp_base)
        elf_table += self.NEW_AUX_ENT(AT_FLAGS, self.elf_flags)
        elf_table += self.NEW_AUX_ENT(AT_ENTRY, self.elf_entry)
        elf_table += self.NEW_AUX_ENT(AT_UID, self.elf_guid)
        elf_table += self.NEW_AUX_ENT(AT_EUID, self.elf_guid)
        elf_table += self.NEW_AUX_ENT(AT_GID, self.elf_guid)
        elf_table += self.NEW_AUX_ENT(AT_EGID, self.elf_guid)
        elf_table += self.NEW_AUX_ENT(AT_HWCAP, self.elf_hwcap)
        elf_table += self.NEW_AUX_ENT(AT_CLKTCK, 100)
        elf_table += self.NEW_AUX_ENT(AT_RANDOM, self.randstraddr)
        elf_table += self.NEW_AUX_ENT(AT_PLATFORM, self.cpustraddr)
        elf_table += self.NEW_AUX_ENT(AT_NULL, 0)

        elf_table += b'\x00' * (0x10 - (new_stack - len(elf_table)) & 0xf)

        self.ql.mem.write(int(new_stack - len(elf_table)), elf_table)
        new_stack = new_stack - len(elf_table)

        # self.ql.dprint(D_INFO, sssssssssssssssssssssssssssssssssssssssssssssssssssssssssss"rdi is : " + hex(ql.register(UC_X86_REG_RDI)))
        # self.ql.register(UC_X86_REG_RDI, new_stack + 8)

        # for i in range(120):
        #     buf = self.ql.mem.read(new_stack + i * 0x8, 8)
        #     self.ql.nprint("0x%08x : 0x%08x " % (new_stack + i * 0x4, self.ql.unpack64(buf)) + ' '.join(['%02x' % i for i in buf]) + '  ' + ''.join([chr(i) if i in string.printable[ : -5].encode('ascii') else '.' for i in buf]))

        self.entry_point = entry_point
        self.elf_entry = loadbase + elfhead['e_entry']
        self.new_stack = new_stack
        self.loadbase = loadbase
        self.ql.mem.add_mapinfo(new_stack, self.ql.stack_address+ql.stack_size, 'rw-', '[stack]')
