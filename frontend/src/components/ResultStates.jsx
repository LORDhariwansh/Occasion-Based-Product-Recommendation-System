import { AlertCircle, SearchX } from "lucide-react";

export function LoadingState() {
  return <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
    {Array.from({ length: 6 }, (_, index) => <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white" key={index}>
      <div className="aspect-[4/3] animate-pulse bg-slate-200" /><div className="space-y-3 p-5"><div className="h-4 w-1/3 animate-pulse rounded bg-slate-200" /><div className="h-6 w-3/4 animate-pulse rounded bg-slate-200" /><div className="h-16 animate-pulse rounded bg-slate-100" /></div></div>)}</div>;
}

export function EmptyState({ message }) {
  return <div className="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center"><SearchX className="mx-auto text-[#155e75]" size={32} strokeWidth={1.6} /><h2 className="mt-4 text-xl font-semibold text-slate-900">No close matches yet</h2><p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-600">{message || "Try a more specific occasion, recipient, or budget."}</p></div>;
}

export function ErrorState({ message }) {
  return <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 text-rose-950"><div className="flex gap-3"><AlertCircle className="shrink-0 text-rose-700" size={21} /><div><h2 className="font-semibold">Could not load recommendations</h2><p className="mt-1 text-sm text-rose-800">{message}</p></div></div></div>;
}
