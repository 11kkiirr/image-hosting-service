from types import TracebackType
from typing import Callable, Optional, Type, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from modules.users.repository import UserRepository
    from modules.accounting.repository import AccountingRepositoryRegistry
    from backend.src.modules.receipts.repository import ReceiptRepository
    from modules.p2p.disputes.repository import DisputeMessageRepository, DisputeRepository
    from modules.notification.repository import ScheduledNotificationRepository
    from modules.p2p.payment_methods.repository import PaymentProviderRepository, PaymentMethodRepository
    from modules.p2p.offers.repository import OffersRepository
    from modules.p2p.deals.repository import DealsRepository
    from modules.p2p.reputation.repository import ReputationRepository

class UnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self):
        self._session = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):  # exc_type, exc_val, exc_tb
        if self._session:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()
            await self._session.close()
            self._session = None

    @property
    def _active_session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                "Сессия UoW не активна. Используйте UnitOfWork в контекстном менеджере 'async with'."
            )
        return self._session

    @property
    def session(self) -> AsyncSession:
        return self._active_session

    @property
    def users(self) -> "UserRepository":
        return UserRepository(self._active_session)

    @property
    def accounting(self) -> "AccountingRepositoryRegistry":
        return AccountingRepositoryRegistry(self._active_session)

    @property
    def receipts(self) -> "ReceiptRepository":
        from backend.src.modules.receipts.repository import ReceiptRepository
        return ReceiptRepository(self._active_session)

    @property
    def disputes(self) -> "DisputeRepository":
        from modules.p2p.disputes.repository import DisputeRepository
        return DisputeRepository(self._active_session)

    @property
    def dispute_messages(self) -> "DisputeMessageRepository":
        from modules.p2p.disputes.repository import DisputeMessageRepository
        return DisputeMessageRepository(self._active_session)

    @property
    def notifications(self) -> "ScheduledNotificationRepository":
        from modules.notification.repository import ScheduledNotificationRepository
        return ScheduledNotificationRepository(self._active_session)

    @property
    def payment_providers(self) -> "PaymentProviderRepository":
        from modules.p2p.payment_methods.repository import PaymentProviderRepository
        return PaymentProviderRepository(self._active_session)

    @property
    def payment_methods(self) -> "PaymentMethodRepository":
        from modules.p2p.payment_methods.repository import PaymentMethodRepository
        return PaymentMethodRepository(self._active_session)

    @property
    def offers(self) -> "OffersRepository":
        from modules.p2p.offers.repository import OffersRepository
        return OffersRepository(self._active_session)

    @property
    def deals(self) -> "DealsRepository":
        from modules.p2p.deals.repository import DealsRepository
        return DealsRepository(self._active_session)

    @property
    def trades(self) -> "DealsRepository":
        return self.deals

    @property
    def reputation(self) -> "ReputationRepository":
        from modules.p2p.reputation.repository import ReputationRepository
        return ReputationRepository(self._active_session)
