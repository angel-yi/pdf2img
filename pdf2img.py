import fitz
from loguru import logger

logger.add('app.log')


def pdf2img(input_paths="./", outputpath="./docimg.pdf", zoom=1.0):
    #  打开PDF文件，生成一个对象
    doc = fitz.open(input_paths)
    logger.info(f"共{doc.pageCount}页")
    for pg in range(doc.pageCount):
        logger.info(f"转换为图片{pg + 1} {doc.pageCount}")
        page = doc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为8，这将为我们生成分辨率提高64倍的图像。
        trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(outputpath + '/tu' + '{:02}.png'.format(pg))


if __name__ == "__main__":
    while 1:
        logger.debug('pdf文件路径')
        file_in = input()
        logger.info(file_in)
        logger.debug('图片保存路径')
        out = input()
        logger.info(out)
        logger.debug('输入图像放大倍数，可回车跳过，默认1.0')
        zoom = input()
        try:
            if zoom:
                zoom = float(zoom)
            pdf2img(file_in, out, zoom)
            logger.info("\n转换完成！")
        except Exception as e:
            logger.exception(f'错误，转换失败：{e}', exc_info=True)
