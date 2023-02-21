import os.path
import threading

import fitz
from loguru import logger
from tqdm import tqdm

logger.add('app.log')


def pdf2img(input_paths="./", outputpath="./docimg.pdf", zoom=1.0, name=None):
    #  打开PDF文件，生成一个对象
    doc = fitz.open(input_paths)
    logger.info(f"共{doc.pageCount}页")
    n = 1
    for pg in tqdm(range(doc.pageCount), desc=input_paths):
        # logger.info(f"转换为图片{pg + 1} {doc.pageCount}")
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为8，这将为我们生成分辨率提高64倍的图像。
        trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(os.path.join(outputpath, f'{name}{n}.png'))
        n += 1
    if n == doc.pageCount:
        logger.info(f'共{doc.pageCount}页, 转换完成{n}页')
    else:
        logger.debug(f'错误，转换失败{doc.pageCount-n}页')
        logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    logger.info("\n转换完成！")


if __name__ == "__main__":
    # save_path = 'output'
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    while 1:
        logger.debug('pdf文件路径/pdf文件夹路径')
        file_in = input()
        logger.info(file_in)
        logger.debug('保存路径')
        save_path = input()
        logger.info(save_path)
        logger.debug('输入图像放大倍数，可回车跳过，默认1.0')
        zoom = input()
        try:
            if zoom:
                zoom = float(zoom)
            else:
                zoom = 1.0
            logger.info(zoom)
            if os.path.isfile(file_in):
                logger.info('输入路径为文件，执行单文件操作')
                if os.path.splitext(file_in)[-1] == '.pdf':
                    dir_name = os.path.basename(file_in)
                    if not os.path.exists(os.path.join(save_path, dir_name)):
                        os.mkdir(os.path.join(save_path, dir_name))
                    pdf2img(file_in, os.path.join(save_path, dir_name), zoom)
                else:
                    logger.error(f'该文件不是pdf文件{os.path.splitext(file_in)}')
            else:
                logger.info('输入路径为文件夹，执行批量文件操作')
                t_list = []
                for pdfifle in os.listdir(file_in):
                    if os.path.splitext(os.path.join(file_in, pdfifle))[-1] == '.pdf':
                        if not os.path.isfile(os.path.join(file_in, pdfifle)):
                            logger.error(f'该文件不是文件: {pdfifle}')
                            continue
                        dir_name = os.path.basename(pdfifle)
                        if not os.path.exists(os.path.join(save_path, dir_name)):
                            os.mkdir(os.path.join(save_path, dir_name))
                        t = threading.Thread(target=pdf2img, args=(os.path.join(file_in, pdfifle), os.path.join(save_path, dir_name), zoom))
                        t_list.append(t)
                    else:
                        logger.error(f'该文件不是pdf文件: {pdfifle}')
                for t in t_list:
                    t.start()
                    t.join()
        except Exception as e:
            logger.exception(f'错误，转换失败：{e}', exc_info=True)
