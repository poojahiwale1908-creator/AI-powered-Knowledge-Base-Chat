import tempfile
from pypdf import PdfReader

class DocumentProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_pdf(self, file):
        if not file or not file.name.lower().endswith('.pdf'):
            return "", {"filename": "unknown", "total_pages": 0}

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file.getvalue())
            tmp_path = tmp.name

        try:
            reader = PdfReader(tmp_path)
            text = ""
            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- Page {i} ---\\n{page_text}\\n"

            import os
            os.unlink(tmp_path)
            return text, {"filename": file.name, "total_pages": len(reader.pages)}
        except:
            import os
            os.unlink(tmp_path)
            return "", {"filename": file.name, "total_pages": 0}

    def chunk_text(self, text, metadata):
        chunks = []
        pages = text.split("--- Page ")
        chunk_id = 0

        for page_section in pages:
            if not page_section.strip():
                continue
            lines = page_section.strip().split('\\n')
            if not lines:
                continue

            page_num = lines[0].split(" ---")[0] if " ---" in lines[0] else "Unknown"
            content = "\\n".join(lines[1:]) if len(lines) > 1 else "\\n".join(lines)

            if not content.strip():
                continue

            words = content.split()
            for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
                chunk_words = words[i:i+self.chunk_size]
                if chunk_words:
                    chunks.append({
                        "id": f"chunk_{chunk_id}",
                        "content": " ".join(chunk_words),
                        "page": page_num,
                        "source": metadata.get("filename", "unknown"),
                        "chunk_index": chunk_id
                    })
                    chunk_id += 1
                if i + self.chunk_size >= len(words):
                    break

        return chunks

    def process_document(self, file):
        text, metadata = self.extract_text_from_pdf(file)
        chunks = self.chunk_text(text, metadata)
        return chunks, metadata
