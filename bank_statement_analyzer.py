import PyPDF2
import re
import argparse

def search_pdf(file_path, keyword):
    results = []
    with open(file_path, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue
            clean_text = text.replace("₹", "").replace(" ", "")
            if re.search(keyword.replace(" ", ""), clean_text, re.IGNORECASE):
                results.append((page_num, text))
    return results

def main():
    parser = argparse.ArgumentParser(description="Search transactions in bank statements PDF")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("keyword", help="Keyword or amount to search")
    args = parser.parse_args()

    matches = search_pdf(args.pdf_path, args.keyword)

    if matches:
        print(f"\nFound {len(matches)} matches for '{args.keyword}':\n")
        for page_num, content in matches:
            print(f"--- Page {page_num + 1} ---")
            for line in content.splitlines():
                if args.keyword.lower().replace(" ", "") in line.lower().replace(" ", ""):
                    print(line)
    else:
        print(f"No matches found for '{args.keyword}'.")

if __name__ == "__main__":
    main()
