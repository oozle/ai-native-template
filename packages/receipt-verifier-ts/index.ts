import { verify } from '@noble/ed25519';

export interface UsageReceipt {
  request_id: string; publisher_id: string; resource_id: string;
  units: { unit: '1k_tokens'|'byte'|'request'; value: number };
  fee_computed: number; ts: string; alg: 'Ed25519'; signature: string;
  hash?: string; agent_decl?: Record<string,unknown>; provenance?: Record<string,unknown>;
}

export async function verifyReceipt(receipt: UsageReceipt, publicKeyHex: string): Promise<boolean> {
  const { signature, ...toSign } = receipt;
  const msg = new TextEncoder().encode(JSON.stringify(toSign));
  const sig = Uint8Array.from(Buffer.from(signature, 'base64'));
  const pub = Uint8Array.from(Buffer.from(publicKeyHex, 'hex'));
  return verify(sig, msg, pub);
}
