import tkinter as tk
from tkinter import ttk, messagebox
import fitz  # PyMuPDF
import os


def extract_pdf():
    # 获取输入的文件名
    pdf_name = entry_pdf.get().strip()
    if not pdf_name:
        messagebox.showerror("错误", "请输入PDF文件名！")
        return

    # 自动补全后缀
    if not pdf_name.endswith(".pdf"):
        pdf_name += ".pdf"

    # 路径检查
    if not os.path.exists(pdf_name):
        messagebox.showerror("错误", f"未找到文件：{pdf_name}\n请把PDF放在本程序同一文件夹！")
        return

    try:
        doc = fitz.open(pdf_name)
        total_text = ""

        # ===== 提取文字 =====
        for page in doc:
            total_text += page.get_text() + "\n"

        # 保存文字
        with open("提取结果_文字.txt", "w", encoding="utf-8") as f:
            f.write(total_text)

        # ===== 提取图片 =====
        img_count = 0
        for page_num, page in enumerate(doc):
            img_list = page.get_images(full=True)
            for img in img_list:
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                # 处理透明通道
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                img_path = f"提取图片_{page_num + 1}_{img_count + 1}.png"
                pix.save(img_path)
                pix = None
                img_count += 1

        doc.close()
        messagebox.showinfo("成功",
                            f"提取完成！\n\n"
                            f"✅ 文字已保存：提取结果_文字.txt\n"
                            f"✅ 图片数量：{img_count} 张")

    except Exception as e:
        messagebox.showerror("异常", f"提取失败：{str(e)}")


# ==================== 界面创建 ====================
root = tk.Tk()
root.title("PDF 文字+图片 提取工具")
root.geometry("500x220")
root.resizable(False, False)

# 样式
style = ttk.Style()
style.configure(".", font=("微软雅黑", 11))

# 标题
label_title = ttk.Label(root, text="PDF 文字 & 图片 提取器", font=("微软雅黑", 16, "bold"))
label_title.pack(pady=15)

# 输入框区域
frame_input = ttk.Frame(root)
frame_input.pack(pady=5)

label_tip = ttk.Label(frame_input, text="请输入PDF文件名（无需输.pdf）：")
label_tip.grid(row=0, column=0, padx=5)

entry_pdf = ttk.Entry(frame_input, width=25, font=("微软雅黑", 11))
entry_pdf.grid(row=0, column=1, padx=5)
entry_pdf.focus()

# 提取按钮
btn_extract = ttk.Button(root, text="开始提取文字和图片", command=extract_pdf)
btn_extract.pack(pady=15)

# 说明
label_info = ttk.Label(root, text="使用说明：把PDF和本程序放在同一文件夹，输入名称即可", foreground="gray")
label_info.pack()

root.mainloop()
