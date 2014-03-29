import os
import urllib

def get_title_author(source_dir):
    ta_file = open("%s/title_author" % source_dir)
    ret = ta_file.read().split('/')
    ta_file.close()

    return ret

def write_chapter(source_dir, dst_dir, volume_name, chapter_name, title_author):
    source_file = None
    dst_file = None
    try:
        source_file = open("%s/%s/%s" % (source_dir, volume_name, chapter_name))
        dst_file = open("%s/%s.html" % (dst_dir, chapter_name), 'w+') 

        dst_file.write(open('t_header.html').read())
        dst_file.write('<div style="color: #000"><h2 style="display: inline">%s</h2> </div>' % title_author[0])
        dst_file.write('<div style="font-size: 12px; margin-bottom: 3em; color: #888">/%s</div>' % title_author[1])
        dst_file.write('<h3 style="margin-bottom: 1em;">%s</h3>' % chapter_name)

        l = source_file.readline()
        while l:
            dst_file.write('<p>%s</p>' % l)
            l = source_file.readline()
    except Exception, e:
        print str(e)
    finally:
        if source_file:
            source_file.close()
        if dst_file:
            dst_file.close()


def build(source_dir, dst_dir):
    catelog_file = open("%s/catelog" % source_dir)
    title_author = get_title_author(source_dir)

    is_volume = True
    chapter_count = 0
    chapter_index = 0
    z_header = open('z_header.html').read()
    z_footer = open('z_footer.html').read()

    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    volume_file = open('%s/index.html' % dst_dir, 'w+')
    volume_file.write(z_header)
    volume_file.write('<div style="color: #000"><h2 style="display: inline">%s</h2> </div>' % title_author[0])
    volume_file.write('<div style="font-size: 12px; margin-bottom: 3em; color: #888">/%s</div>' % title_author[1])


    volume_name = None
    clc = catelog_file.readline()
    while clc:
        if is_volume:
            volume_name = clc.rstrip('\n')
            volume_file.write('<h3>%s</h3>\n' % volume_name)
            volume_file.write('<ul>\n')
            chapter_count = int(catelog_file.readline()) 
            chapter_index = 0

            if chapter_count != 0:
                is_volume = False
        else:
            clc = clc.rstrip('\n')
            write_chapter(source_dir, dst_dir, volume_name, clc, title_author)
            volume_file.write('<a href="%s"><li>%s</li></a>' % ("%s.html" % clc, clc))
            if chapter_index == (chapter_count - 1):
                volume_file.write('</ul>\n')
                is_volume = True
            chapter_index += 1
        clc = catelog_file.readline()
    
    volume_file.write(z_footer)
    volume_file.close()

if __name__ == "__main__":
    source_dir = "/tmp/pp"
    dst_dir = "/tmp/fkk"

    build(source_dir, dst_dir)
    
