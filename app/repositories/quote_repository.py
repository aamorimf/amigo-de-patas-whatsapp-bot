from sqlalchemy.orm import Session
from app.models.schema import Quote

def get_or_create_quote(db: Session, client_id: int) -> Quote:
    quote = db.query(Quote).filter(Quote.client_id == client_id, Quote.status == "DRAFT").first()
    if not quote:
        quote = Quote(client_id=client_id)
        db.add(quote)
        db.commit()
        db.refresh(quote)
    return quote

def reset_quote(db: Session, client_id: int) -> Quote:
    # Delete current draft or just clear fields
    quote = db.query(Quote).filter(Quote.client_id == client_id, Quote.status == "DRAFT").first()
    if quote:
        quote.setor = None
        quote.produto = None
        quote.tamanho = None
        quote.quantidade = None
        db.commit()
        db.refresh(quote)
    else:
        quote = get_or_create_quote(db, client_id)
    return quote

def update_quote_field(db: Session, quote: Quote, field: str, value: str):
    if hasattr(quote, field):
        setattr(quote, field, value)
        db.commit()
        db.refresh(quote)
