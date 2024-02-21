from typing import List, Optional

from fastapi import Depends, HTTPException
import fastapi
from sqlmodel import select

from db.db_setup import get_session, Session
from utils.get_all_hypervisors import fetch_esxi_from_vc, update_or_create_esxi
from models.esxi import ESXCount, ESXi
from utils.vcenter.vcenter_connection import VCenter


router = fastapi.APIRouter()


@router.get("/esxi/{esxi_name}", response_model=ESXi, status_code=200)
def get_single_esxi(*, session: Session = Depends(get_session), esxi_name: str):
    esxi = session.exec(select(ESXi).where(ESXi.name == esxi_name)).first()
    if not esxi:
        raise HTTPException(status_code=404, detail="ESXi server not found")
    return esxi.dict()


@router.get("/esxi", response_model=List[ESXi], status_code=200)
def get_esxi_from_db(*,
                     session: Session = Depends(get_session),
                     cluster: Optional[str] = None,):
    query = select(ESXi)
    if cluster:
        query = query.where(ESXi.cluster == cluster)
    esxi = session.exec(query).all()
    if not esxi:
        raise HTTPException(status_code=404, detail="No ESXi server found in the database")
    return esxi


@router.post("/esxis/{vcenter}", response_model=ESXCount, status_code=201)
def fetch_esxi_from_vcenter(*, session: Session = Depends(get_session), vcenter: str):
    fetched_esxi = fetch_esxi_from_vc(vcenter)
    update_or_create_esxi(session, fetched_esxi)
    return ESXCount(count=len(fetched_esxi))